import pandas as pd
import streamlit as st
import plotly.express as px

from src.database import init_db, save_complaint, list_complaints, get_complaint
from src.pipeline import analyze_complaint
from src.classification import load_classifier, train_classifier
from src.evaluation import evaluate_classifier
from src.config import GEMINI_API_KEY

st.set_page_config(page_title="CivicAI | NLP Grievance Analysis", page_icon="🏛️", layout="wide")
init_db()

CATEGORIES = [
    "Water Supply", "Electricity", "Roads & Infrastructure", "Waste Management",
    "Sanitation", "Public Transport", "Street Lighting", "Healthcare",
    "Public Safety", "Environment", "Housing", "Government Services"
]

st.sidebar.title("🏛️ CivicAI")
page = st.sidebar.radio("Navigate", [
    "Dashboard", "Analyze Complaint", "Batch Analysis",
    "Complaint History", "Similar Complaints", "Model Evaluation", "About Project"
])
st.sidebar.caption("NLP mini project • Local demo")
st.sidebar.markdown("---")
st.sidebar.caption("Gemini: " + ("Configured" if GEMINI_API_KEY else "Optional / not configured"))

def show_result(result):
    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted category", result["category"])
    c2.metric("Urgency", result["urgency"])
    c3.metric("Recommended department", result["department"])
    st.markdown("#### AI / NLP summary")
    st.write(result["summary"])
    st.markdown("#### Extracted information")
    entities = result.get("entities", [])
    if entities:
        st.dataframe(pd.DataFrame(entities), use_container_width=True, hide_index=True)
    else:
        st.info("No entities confidently extracted from this text.")
    st.markdown("#### Preprocessing")
    st.write("**Normalized text:**", result["normalized_text"])
    st.write("**Tokens:**", ", ".join(result["tokens"]) or "No tokens")
    st.markdown("#### Category scores")
    scores = result.get("class_scores", {})
    if scores:
        sdf = pd.DataFrame([{"Category": k, "Score": v} for k, v in scores.items()]).sort_values("Score", ascending=False)
        st.dataframe(sdf, use_container_width=True, hide_index=True)
    st.caption(f"Classification method: {result['classification_method']} • Summary method: {result['summary_method']}")
    similar = result.get("similar_complaints", [])
    if similar:
        st.markdown("#### Potentially similar previous complaints")
        st.dataframe(pd.DataFrame(similar), use_container_width=True, hide_index=True)

if page == "Dashboard":
    st.title("CivicAI")
    st.subheader("AI-powered government grievance classification and routing")
    st.write("Analyze citizen complaints using NLP, machine learning, entity extraction, urgency detection, summarization, and semantic similarity.")
    rows = list_complaints(limit=1000)
    df = pd.DataFrame(rows)
    if df.empty:
        a,b,c,d = st.columns(4)
        a.metric("Complaints analyzed", 0); b.metric("High / critical", 0); c.metric("Categories covered", 0); d.metric("Potential duplicates", 0)
        st.info("No complaint history yet. Open **Analyze Complaint** to run your first example.")
    else:
        a,b,c,d = st.columns(4)
        a.metric("Complaints analyzed", len(df))
        b.metric("High / critical", int(df["urgency"].isin(["HIGH","CRITICAL"]).sum()))
        c.metric("Categories covered", int(df["category"].nunique()))
        d.metric("Potential duplicate flags", int(df["similar_count"].fillna(0).sum()))
        left,right = st.columns(2)
        with left:
            st.plotly_chart(px.bar(df["category"].value_counts().rename_axis("Category").reset_index(name="Count"), x="Category", y="Count", title="Complaints by category"), use_container_width=True)
        with right:
            st.plotly_chart(px.pie(df, names="urgency", title="Urgency distribution"), use_container_width=True)
        st.markdown("#### Recent complaints")
        st.dataframe(df[["complaint_id","created_at","category","urgency","department","status"]].head(10), use_container_width=True, hide_index=True)

elif page == "Analyze Complaint":
    st.title("Analyze a complaint")
    st.write("Enter a grievance in natural language. CivicAI will run the available NLP components and store the result locally.")
    example = "There has been no water supply in Ward 14, Gandhi Nagar for the last five days. Around forty families are affected, and the water tanker has not arrived since Monday."
    text = st.text_area("Complaint text", value=example, height=150, placeholder="Describe the issue, location, duration, and impact...")
    if st.button("Analyze complaint", type="primary", use_container_width=True):
        if not text.strip():
            st.error("Please enter a complaint before analyzing.")
        else:
            with st.spinner("Running NLP pipeline..."):
                result = analyze_complaint(text, persist=True)
            st.success(f"Analysis saved. Complaint ID: {result['complaint_id']}")
            show_result(result)

elif page == "Batch Analysis":
    st.title("Batch complaint analysis")
    st.write("Upload a CSV with a `complaint_text` column. Analysis results can be downloaded as a CSV.")
    upload = st.file_uploader("Upload complaints CSV", type=["csv"])
    if upload:
        try:
            input_df = pd.read_csv(upload)
            if "complaint_text" not in input_df.columns:
                st.error("CSV must contain a `complaint_text` column.")
            else:
                st.dataframe(input_df.head(10), use_container_width=True, hide_index=True)
                if st.button("Analyze all rows", type="primary"):
                    results = []
                    progress = st.progress(0)
                    valid = input_df["complaint_text"].fillna("").astype(str).tolist()
                    for i, complaint in enumerate(valid):
                        if complaint.strip():
                            results.append(analyze_complaint(complaint, persist=True))
                        progress.progress((i+1)/max(1,len(valid)))
                    out = pd.DataFrame([{
                        "complaint_id": r["complaint_id"], "complaint_text": r["original_text"],
                        "category": r["category"], "urgency": r["urgency"], "department": r["department"],
                        "location": next((e["value"] for e in r["entities"] if e["label"]=="LOCATION"), ""),
                        "summary": r["summary"], "classification_method": r["classification_method"]
                    } for r in results])
                    st.success(f"Analyzed {len(out)} complaints.")
                    st.dataframe(out, use_container_width=True, hide_index=True)
                    st.download_button("Download results CSV", out.to_csv(index=False).encode("utf-8"), "civicai_batch_results.csv", "text/csv")
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")

elif page == "Complaint History":
    st.title("Complaint history")
    rows = list_complaints(limit=1000)
    df = pd.DataFrame(rows)
    if df.empty:
        st.info("No complaints saved yet.")
    else:
        search = st.text_input("Search by ID, text, category, or department")
        status = st.selectbox("Status filter", ["All"] + sorted(df["status"].dropna().unique().tolist()))
        if status != "All":
            df = df[df["status"] == status]
        if search.strip():
            mask = df.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
            df = df[mask]
        st.dataframe(df[["complaint_id","created_at","original_text","category","urgency","department","status"]], use_container_width=True, hide_index=True)
        chosen = st.selectbox("Open complaint", [""] + df["complaint_id"].tolist())
        if chosen:
            item = get_complaint(chosen)
            if item:
                st.json(item)
                new_status = st.selectbox("Update status", ["SUBMITTED","AI_ANALYZED","ASSIGNED","IN_PROGRESS","RESOLVED","CLOSED","REOPENED"], index=["SUBMITTED","AI_ANALYZED","ASSIGNED","IN_PROGRESS","RESOLVED","CLOSED","REOPENED"].index(item["status"]))
                if st.button("Save status"):
                    from src.database import update_status
                    update_status(chosen, new_status)
                    st.success("Status updated.")
                    st.rerun()
        st.download_button("Export history CSV", df.to_csv(index=False).encode("utf-8"), "civicai_history.csv", "text/csv")

elif page == "Similar Complaints":
    st.title("Similar complaints")
    rows = list_complaints(limit=1000)
    if len(rows) < 2:
        st.info("Analyze at least two complaints to compare semantic similarity.")
    else:
        st.write("The app flags possible matches; it does not automatically merge complaints.")
        from src.similarity import find_similar
        query = st.text_area("Enter text to compare against saved complaints", height=100)
        if st.button("Find similar complaints", type="primary"):
            st.dataframe(pd.DataFrame(find_similar(query, rows, exclude_id=None)), use_container_width=True, hide_index=True)

elif page == "Model Evaluation":
    st.title("Model evaluation")
    st.write("Evaluation uses the included labelled sample dataset. Synthetic sample data is for demonstration only and is not evidence of real-world performance.")
    if st.button("Evaluate baseline model", type="primary"):
        with st.spinner("Training and evaluating a held-out test split..."):
            report = evaluate_classifier()
        st.metric("Accuracy", f"{report['accuracy']:.3f}")
        st.json(report["classification_report"])
        st.plotly_chart(px.imshow(report["confusion_matrix"], x=report["labels"], y=report["labels"], text_auto=True, aspect="auto", title="Confusion matrix"), use_container_width=True)
        st.caption("These scores are calculated on the included synthetic dataset; use a representative, independently labelled dataset for meaningful evaluation.")

else:
    st.title("About CivicAI")
    st.markdown("""
    **Problem:** Government departments receive large volumes of unstructured complaints. Manual categorization and routing can be slow.

    **Objectives:** Classify grievances, extract useful entities, estimate urgency, recommend departments, summarize complaints, and find potentially similar records.

    **NLP workflow:** Text normalization → TF-IDF classification → entity extraction → urgency estimation → department mapping → summarization → semantic similarity → SQLite persistence.

    **Important limitations:** The included dataset is synthetic. Urgency and entity extraction are assistive estimates. Similarity does not prove two reports describe the same event. Gemini summarization is optional.
    """)
    st.markdown("### Technology")
    st.write("Python • Streamlit • scikit-learn • spaCy (optional) • Sentence Transformers (optional) • Gemini (optional) • SQLite • Plotly")
