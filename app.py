import streamlit as st
import joblib

st.set_page_config(page_title="URL Güvenlik Analizi", page_icon="🛡️")

st.title("🛡️ Siber Güvenlik: Akıllı URL Kontrol Aracı")
st.markdown("Şüphelendiğiniz linkleri buraya yapıştırarak yapay zeka ile analiz edebilirsiniz.")

kullanici_linki = st.text_input("Analiz edilecek linki girin:")

# Gerçek dünya sistemlerindeki "Beyaz Liste" (Whitelist) uygulaması
beyaz_liste = ["youtube.com", "google.com", "apple.com", "github.com", "sakarya.edu.tr", "linkedin.com"]

if st.button("Analiz Et"):
    if kullanici_linki.strip() == "":
        st.warning("Lütfen geçerli bir link girin!")
    else:
        # Önce Beyaz Liste kontrolü yapıyoruz
        is_whitelisted = any(domain in kullanici_linki.lower() for domain in beyaz_liste)
        
        if is_whitelisted:
            st.success("✅ SONUÇ: GÜVENLİ. (Durum: %0.0 Risk)")
            st.info("👍 Bu site sistemimizdeki güvenilir kurumlar listesindedir (Whitelist). Yapay zeka taramasına gerek duyulmadı.")
        else:
            # Beyaz listede yoksa Yapay Zeka modelini devreye sok
            try:
                nlp_model = joblib.load('models/nlp_model.joblib')
                tfidf = joblib.load('models/tfidf_vectorizer.joblib')
                
                url_tfidf = tfidf.transform([kullanici_linki])
                prediction = nlp_model.predict(url_tfidf)[0]
                probability = nlp_model.predict_proba(url_tfidf)[0][1] * 100
                
                st.markdown("### ⏳ Yapay Zeka Analiz Ediyor...")
                
                if prediction == 1:
                    st.error(f"🚨 SONUÇ: RİSKLİ! (Zararlı olma ihtimali: %{probability:.1f})")
                    st.warning("⚠️ DİKKAT: Bu linke TIKLAMAYIN ve kişisel bilgilerinizi PAYLAŞMAYIN.")
                else:
                    st.success(f"✅ SONUÇ: GÜVENLİ. (Zararlı olma ihtimali: %{probability:.1f})")
                    st.info("👍 Site güvenli görünüyor, giriş yapabilirsiniz.")
                    
            except FileNotFoundError:
                st.error("Model dosyaları bulunamadı. Lütfen dosya yollarını kontrol edin.")