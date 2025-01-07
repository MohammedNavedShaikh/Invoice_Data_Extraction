import streamlit as st
from dotenv import load_dotenv
from utils import create_docs
from logging_config import logger

def main():
    load_dotenv()

    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot")
    st.subheader("I can help you in extracting invoice data")

    pdf_files = st.file_uploader("Upload invoices here, only PDF files allowed", type=["pdf"], accept_multiple_files=True)

    submit = st.button("Extract Data")

    if submit:
        if pdf_files:
            with st.spinner('Wait for it...'):
                try:
                    logger.info("Starting data extraction process.")
                    df = create_docs(pdf_files)
                    if not df.empty:
                        logger.info("Data extracted successfully.")
                        st.write(df.head())

                        data_as_csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "Download data as CSV",
                            data_as_csv,
                            "extracted_data.csv",
                            "text/csv",
                            key="download-csv",
                        )
                        st.success("Data extraction complete!")
                    else:
                        logger.warning("No data could be extracted from the uploaded PDFs.")
                        st.warning("No data could be extracted. Please check your PDFs.")
                except Exception as e:
                    logger.error(f"Error during data extraction: {str(e)}", exc_info=True)
                    st.error(f"Error during extraction: {str(e)}")
        else:
            logger.warning("No PDF files uploaded.")
            st.warning("Please upload one or more PDF files.")

if __name__ == '__main__':
    logger.info("Invoice Extraction Bot started.")
    main()
