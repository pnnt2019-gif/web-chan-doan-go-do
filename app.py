import os
import streamlit as st
from PIL import Image  # Đã thêm thư viện này để đọc ảnh

try:
    from ultralytics import YOLO
except ImportError:
    st.error("Thiếu thư viện ultralytics")
    st.stop()

# Tải mô hình YOLO (Sử dụng cache để tiết kiệm RAM)
@st.cache_resource
def load_model():
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
    return YOLO(MODEL_PATH)

# Cấu hình trang web
st.set_page_config(page_title="Web Tích hợp CSDL Bệnh lá Gõ đỏ", layout="wide")

# ==========================================
# CƠ SỞ DỮ LIỆU THÔNG TIN BỆNH HẠI 
# ==========================================
disease_database = {
    "Phấn trắng": {
        "Trọng tâm": True,
        "Nguyên nhân": "Do điều kiện thời tiết ẩm ướt, thiếu ánh sáng, sương mù nhiều và mật độ gieo ươm cây quá dày đặc tạo tiểu khí hậu thuận lợi cho mầm bệnh phát triển.",
        "Tác nhân": "Nấm Oidium sp.",
        "Triệu chứng": "Xuất hiện lớp bột màu trắng xám bao phủ trên bề mặt lá và chồi non. Lá bị nhiễm bệnh nặng thường có hiện tượng nhăn nheo, biến dạng, khô và rụng sớm, làm giảm khả năng quang hợp của cây.",
        "Biện pháp phòng trừ": "Cắt tỉa và thu gom các cành, lá bị bệnh mang đi tiêu hủy xa vườn ươm. Chủ động phun phòng hoặc trị bệnh bằng các loại thuốc trừ nấm gốc lưu huỳnh, Anvil 5SC khi bệnh chớm xuất hiện."
    },
    "Đốm lá": {
        "Trọng tâm": True,
        "Nguyên nhân": "Môi trường vườn ươm đọng nước, độ ẩm không khí cao, mầm bệnh lây lan mạnh qua gió và nước mưa/nước tưới bám trên mặt lá.",
        "Tác nhân": "Nấm Stemphylium sp.",
        "Triệu chứng": "Trên phiến lá xuất hiện các vết đốm màu nâu đen đến đen, ban đầu nhỏ gọn sau đó lan rộng. Xung quanh vết đốm có thể có quầng vàng. Bệnh phát triển mạnh làm lá khô cháy và rụng hàng loạt.",
        "Biện pháp phòng trừ": "Đảm bảo mật độ cây thông thoáng. Vệ sinh vườn, thu dọn tàn dư thực vật. Sử dụng các loại thuốc bảo vệ thực vật gốc đồng (như Mancozeb, Daconil) để phun xịt."
    },
    "Cháy lá lớn": {
        "Trọng tâm": False,
        "Nguyên nhân": "Do nấm gây hại xâm nhập qua vết thương hở trên lá hoặc do nắng gắt chiếu trực tiếp sau khi mưa/tưới đọng nước làm cháy mô tế bào.",
        "Triệu chứng": "Vết cháy lớn lan rộng từ mảng lá, thường có màu nâu xám, làm khô một phần lớn diện tích phiến lá."
    },
    "Cháy lá nhỏ": {
        "Trọng tâm": False,
        "Nguyên nhân": "Thường do nấm thứ cấp tấn công vào các mô lá yếu hoặc do thiếu hụt dinh dưỡng cục bộ trên phiến lá.",
        "Triệu chứng": "Các đốm cháy nhỏ rải rác trên phiến lá, màu nâu nhạt, không liên kết thành mảng lớn như bệnh cháy lá lớn."
    },
    "Cháy mép lá": {
        "Trọng tâm": False,
        "Nguyên nhân": "Cây bị mất nước đột ngột, gió khô nóng hoặc do nồng độ phân bón/thuốc hóa học bám ở phần mép lá quá cao gây ngộ độc.",
        "Triệu chứng": "Phần viền mép lá bị khô, chuyển sang màu nâu đen và quăn lại, trong khi phần giữa phiến lá vẫn giữ màu xanh."
    },
    "Cháy ngọn lá": {
        "Trọng tâm": False,
        "Nguyên nhân": "Chênh lệch nhiệt độ ngày đêm lớn, hoặc sương muối làm tổn thương trực tiếp đến các tế bào non ở chóp lá.",
        "Triệu chứng": "Phần chóp lá (ngọn lá) bị khô héo, chuyển màu nâu, vết cháy có thể lan dần xuống dọc theo gân chính của lá."
    },
    "Rỉ sắt": {
        "Trọng tâm": False,
        "Nguyên nhân": "Độ ẩm không khí cao, mầm bệnh phát triển và lây lan mạnh mẽ nhất vào các giai đoạn giao mùa.",
        "Triệu chứng": "Mặt dưới lá xuất hiện các ổ bào tử nổi lên có màu vàng cam hoặc nâu đỏ giống như màu rỉ sắt, làm lá suy yếu và rụng."
    },
    "Mắt cua": {
        "Trọng tâm": False,
        "Nguyên nhân": "Vi khuẩn hoặc nấm tấn công mạnh trong điều kiện môi trường mưa nhiều, lây lan chủ yếu qua các giọt nước bắn.",
        "Triệu chứng": "Vết bệnh có hình tròn, kích thước nhỏ, tâm vết bệnh có màu xám trắng và viền ngoài màu nâu đậm nhìn giống như mắt cua."
    },
    "Thối cổ rễ": {
        "Trọng tâm": False,
        "Nguyên nhân": "Nền đất tại bầu ươm quá ẩm ướt, ứ đọng nước lâu ngày tạo điều kiện lý tưởng cho nấm đất tấn công vùng rễ.",
        "Triệu chứng": "Phần thân sát mặt đất (cổ rễ) bị úng nước, chuyển sang màu nâu đen, thối rữa khiến toàn bộ phần thân lá phía trên héo rũ và chết gục."
    }
}

# ==========================================
# THANH ĐIỀU HƯỚNG (SIDEBAR)
# ==========================================
st.sidebar.title("Hệ thống Web Tích hợp CSDL")
page = st.sidebar.radio("Chọn chức năng:", ["Chẩn đoán bệnh", "Danh mục bệnh hại"])

st.sidebar.markdown("---")
st.sidebar.write("**Tác giả:** Phạm Nguyễn Nhật Thành")
st.sidebar.write("**Lớp:** DH22LN")
st.sidebar.write("**MSSV:** 22114022")

# ==========================================
# TRANG 1: CHẨN ĐOÁN BỆNH
# ==========================================
if page == "Chẩn đoán bệnh":
    st.title("Tích hợp cơ sở dữ liệu chẩn đoán bệnh lá Gõ đỏ (Nhóm I)")
    st.write("Tải hình ảnh lá bệnh lên hệ thống để tiến hành nhận diện và truy xuất cơ sở dữ liệu.")
    
    uploaded_file = st.file_uploader("Chọn ảnh định dạng JPG, PNG...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ảnh gốc tải lên")
            image = Image.open(uploaded_file)
            
            # --- Ép dung lượng ảnh nhỏ lại để chống tràn RAM ---
            image.thumbnail((640, 640)) 
            # ---------------------------------------------------
            
            st.image(image, width=350)
            
        if st.button('Tiến hành chẩn đoán', type="primary"):
            with st.spinner('Mô hình đang quét và trích xuất đặc trưng...'):
                try:
                    model = load_model()
                    results = model(image)
                    
                    detected_classes = [model.names[int(c)] for c in results[0].boxes.cls]
                    res_plotted = results[0].plot()
                    
                    with col2:
                        st.subheader("Kết quả khoanh vùng")
                        st.image(res_plotted, width=350)
                        
                    st.divider()
                    st.subheader("📝 Báo cáo chẩn đoán chi tiết")
                    
                    if len(detected_classes) == 0:
                        st.info("Không phát hiện vết bệnh nào trên ảnh.")
                    else:
                        unique_diseases = list(set(detected_classes))
                        
                        for disease in unique_diseases:
                            if disease in disease_database:
                                info = disease_database[disease]
                                st.markdown(f"### Bệnh phát hiện: **{disease}**")
                                st.write(f"- **Nguyên nhân:** {info['Nguyên nhân']}")
                                if info["Trọng tâm"]:
                                    st.write(f"- **Tác nhân:** {info['Tác nhân']}")
                                st.write(f"- **Triệu chứng:** {info['Triệu chứng']}")
                                if info["Trọng tâm"]:
                                    st.write(f"- **Biện pháp phòng trừ:** {info['Biện pháp phòng trừ']}")
                            else:
                                st.markdown(f"### Bệnh phát hiện: **{disease}**")
                                st.write("- *Đang cập nhật thêm thông tin cơ sở dữ liệu.*")
                                
                except Exception as e:
                    st.error(f"Có lỗi xảy ra: Hãy đảm bảo file 'best.pt' nằm cùng thư mục và ảnh hợp lệ. Chi tiết lỗi: {e}")

# ==========================================
# TRANG 2: DANH MỤC BỆNH HẠI
# ==========================================
elif page == "Danh mục bệnh hại":
    st.title("📚 Danh mục bệnh hại trên lá Gõ đỏ (Nhóm I)")
    st.write("Tổng hợp các bệnh hại ghi nhận qua công tác điều tra thực địa để xây dựng cơ sở dữ liệu:")
    
    # Duyệt qua toàn bộ cơ sở dữ liệu để in thông tin
    for ten_benh, thong_tin in disease_database.items():
        # Các bệnh trọng tâm sẽ tự động mở rủ xuống (expanded=True)
        with st.expander(f"Bệnh: {ten_benh}", expanded=thong_tin["Trọng tâm"]):
            st.write(f"**- Nguyên nhân:** {thong_tin['Nguyên nhân']}")
            
            # Chỉ bệnh trọng tâm mới in Tác nhân
            if thong_tin["Trọng tâm"]:
                st.write(f"**- Tác nhân:** {thong_tin['Tác nhân']}")
                
            st.write(f"**- Triệu chứng:** {thong_tin['Triệu chứng']}")
            
            # Chỉ bệnh trọng tâm mới in Biện pháp phòng trừ
            if thong_tin["Trọng tâm"]:
                st.write(f"**- Biện pháp phòng trừ:** {thong_tin['Biện pháp phòng trừ']}")
