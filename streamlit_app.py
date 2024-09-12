import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

# Streamlit 앱 제목
st.title("PDF to JPG 변환기 (PyMuPDF 사용)")

# 사용자로부터 PDF 파일 업로드 받기
uploaded_pdf = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")

if uploaded_pdf is not None:
    # PDF 문서 열기
    pdf_document = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    
    # 페이지 선택 슬라이더
    page_num = st.slider("변환할 페이지 번호를 선택하세요", 1, pdf_document.page_count)
    
    # 변환 버튼
    if st.button("PDF 변환"):
        # 페이지 선택
        page = pdf_document.load_page(page_num - 1)  # 0-based index
        
        # 페이지를 이미지로 변환
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 이미지 버퍼에 저장
        img_buffer = BytesIO()
        img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)

        # 이미지 표시
        st.image(img, caption=f"Page {page_num}")

        # 다운로드 버튼 제공
        st.download_button(
            label="JPG 이미지 다운로드",
            data=img_buffer,
            file_name=f"page_{page_num}.jpg",
            mime="image/jpeg"
        )
