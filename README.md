# <p align="center">🐺 [Turkhackteam.org](https://www.turkhackteam.org) — Siber Kurtların Karargahı 🐺</p>

<p align="center">
  <img src="https://img.shields.io/badge/Yazar-AltayHR-red?style=for-the-badge&logo=github&logoColor=white&labelColor=black">
  <img src="https://img.shields.io/badge/Platform-Termux%20%2F%20Linux%20%2F%20Windows-0078D4?style=for-the-badge&logo=linux&logoColor=white">
  <img src="https://img.shields.io/badge/Dil-Python%203.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Sürüm-v3.0%20Stable-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/Lisans-Özel%20Mülk%20%2F%20Proprietary-gold?style=flat-square">
  <img src="https://img.shields.io/badge/Güvenlik-Test%20Edildi-orange?style=flat-square">
</p>

---

## 🗺️ İÇİNDEKİLER / TABLE OF CONTENTS
* [🇹🇷 Türkçe Dokümantasyon](#-türkçe-dokümantasyon)
* [🇺🇸 English Documentation](#-english-documentation)
* [🇷🇺 Русская Документация](#-русская-документация)
* [Arabic Documentation / الوثائق العربية 🇦🇷](#-arabic-documentation---الوثائق-العربية)

---

## 🇹🇷 TÜRKÇE DOKÜMANTASYON

### 📌 Proje Hakkında
**Auto_Dork (Dork Hunter)**, siber güvenlik dünyasında pasif bilgi toplama (OSINT) ve zafiyet tespiti süreçlerini hızlandırmak amacıyla **AltayHR** tarafından özel olarak geliştirilmiş proaktif bir istihbarat aracıdır. Gelişmiş dork motoru sayesinde arama motorlarının dizinlerini tarayarak hedef sistemlere ait kritik URL yapılarını, potansiyel veri sızıntılarını, açık unutulmuş yönetim (admin) panellerini ve yapılandırma hatalarını saniyeler içinde tespit eder.

### 🛠️ Öne Çıkan Özellikler
* 📊 **Geniş Dork Havuzu:** İçerisinde entegre olarak gelen 100'den fazla güncel ve optimize edilmiş dork kategorisi.
* ⚡ **Çoklu Tarama Modu:** İster tek bir zafiyet türüne odaklanın, ister tam otomatik mod ile tüm kategorileri taratın.
* 💾 **Otomatik Raporlama:** Taramalar bittiğinde sonuçları otomatik olarak ayııklayıp düzenli `.txt` dosyaları halinde kaydeder.
* 🔓 **Gelişmiş Filtreleme:** Arama motorlarının temiz yapılarını analiz ederek yanıltıcı sonuçları en aza indirir.

### 🚀 Kurulum ve Çalıştırma
Termux, Linux veya Windows (Git Bash) terminalinizi açın ve aşağıdaki komut dizisini sırasıyla kopyalayıp yapıştırın:

```bash
git clone [https://github.com/ThT0AltayHR/Auto_Dork.git](https://github.com/ThT0AltayHR/Auto_Dork.git)
cd Auto_Dork
bash setup.sh
python dork_tool.py

📜 Lisans ve Hak Sahipliği
⚠️ DİKKAT: KOPYALANMASI KESİNLİKLE YASAKTIR.
Bu yazılımın kaynak kodları, algoritması ve mimarisi AltayHR'ye ait olup özel lisans altındadır. Kodların kısmen veya tamamen kopyalanması, klonlanarak farklı isimlerle yeniden yayımlanması, izinsiz ticari amaçla dağıtılması veya başka projelere entegre edilmesi durumunda yasal süreç başlatılacaktır.
⚖️ Yasal Uyarı ve Sorumluluk Reddi
Bu araç yalnızca yasal sınır çerçevesindeki sızma testleri, siber defans analizleri ve eğitim amaçlı laboratuvar ortamlarında kullanılmak üzere tasarlanmıştır. Aracın yetkisiz sistemler üzerinde kullanılmasından doğabilecek her türlü hukuki, cezai ve maddi sorumluluk doğrudan kullanıcıya aittir. Yapımcı (AltayHR) ve Turkhackteam topluluğu hiçbir zarardan sorumlu tutulamaz.
🇺🇸 ENGLISH DOCUMENTATION
📌 About the Project
Auto_Dork (Dork Hunter) is a proactive intelligence tool specifically designed and coded by AltayHR to accelerate open-source intelligence (OSINT) and vulnerability identification processes in the cybersecurity domain. Powered by an advanced dork-parsing engine, it scans search engine indexes to reveal critical URL parameters, exposure points, hidden administration panels, and system misconfigurations in seconds.
🛠️ Key Features
📊 Massive Dork Database: More than 100 predefined, fully optimized query configurations.
⚡ Flexible Automation: Target single analytical modes or initiate deep, full-scale system auditing.
💾 Instant Reporting: Generated output lists are systematically sanitized and exported into structural .txt records.
🔓 Evasion & Optimization: Filters out noise and false positives for precision.
🚀 Installation & Execution
Launch your Termux environment or Linux terminal, then execute the following stack setup precisely:

git clone [https://github.com/ThT0AltayHR/Auto_Dork.git](https://github.com/ThT0AltayHR/Auto_Dork.git)
cd Auto_Dork
bash setup.sh
python dork_tool.py

📜 Intellectual Property & Licensing
⚠️ PROPRIETARY NOTICE: REPLICATION STRICTLY FORBIDDEN.
This codebase, core structure, and logical flow are the intellectual property of AltayHR. Partial or full unauthorized copying, commercial reselling, repackaging under different tags, or unlicensed distribution is strictly prohibited. Legal enforcement will be pursued upon violation.
⚖️ Legal Disclaimer
This software is provided exclusively for legitimate cybersecurity assessments, educational purposes, and white-hat testing environments. The developer (AltayHR) and the Turkhackteam network accept no responsibility or liability for unauthorized activities or secondary damages inflicted by this utility. The end-user operates it at their own risk.
🇷🇺 РУССКАЯ ДОКУМЕНТАЦИЯ
📌 О проекте
Auto_Dork (Dork Hunter) — это передовой инструмент разведки и поиска уязвимостей на основе открытых источников (OSINT), разработанный исследователем AltayHR. С помощью оптимизированного поискового движка утилита мгновенно выявляет скрытые административные интерфейсы, утечки системных логов, критические параметры URL и уязвимые конфигурации веб-серверов.
🛠️ Основные возможности
📊 База данных дорков: Более 100 категорий фильтрации поисковых запросов.
⚡ Многофункциональность: Поддержка точечного сканирования или полностью автоматического глобального аудита.
💾 Структурированный экспорт: Результаты автоматически очищаются и сохраняются в отчеты .txt.
🚀 Установка и запуск
Откройте терминал Termux или дистрибутив Linux и выполните следующие команды по порядку:

git clone [https://github.com/ThT0AltayHR/Auto_Dork.git](https://github.com/ThT0AltayHR/Auto_Dork.git)
cd Auto_Dork
bash setup.sh
python dork_tool.py

📜 Лицензия и защита авторских прав
⚠️ ВНИМАНИЕ: КОПИРОВАНИЕ И ПЛАГИАТ СТРОГО ЗАПРЕЩЕНЫ.
Исходный код и архитектура этого инструмента защищены авторским правом разработчика AltayHR. Любая модификация кода, публикация под чужим именем или незаконная интеграция в сторонние проекты повлечет за собой соответствующие меры защиты интеллектуальной собственности.
⚖️ Правовая оговорка
Этот инструмент предназначен исключительно для проведения санкционированного тестирования на проникновение и обучения. Разработчик (AltayHR) и сообщество Turkhackteam не несут ответственности за любые незаконные действия пользователей или ущерб сторонним инфраструктурам.
🇦🇷 ARABIC DOCUMENTATION - الوثائق العربية
📌 نبذة عن الأداة
أداة Auto_Dork (Dork Hunter) هي عبارة عن نظام ذكي متقدم لجمع المعلومات مفتوحة المصدر (OSINT) وفحص الثغرات، تم تطويره وبرمجته بشكل خاص بواسطة AltayHR. تقوم الأداة بفحص فهارس محركات البحث بدقة عالية للكشف عن روابط URL الحساسة، وتسريبات البيانات، ولوحات التحكم الخفية، والأخطاء البرمجية في الأنظمة خلال ثوانٍ معدودة.
🛠️ الميزات الرئيسية
📊 قاعدة بيانات ضخمة: تحتوي على أكثر من 100 فئة من الـ Dorks المحدثة والمحسنة بالكامل.
⚡ أتمتة مرنة: إمكانية تشغيل الفحص على ثغرة معينة أو تفعيل الفحص التلقائي الشامل لجميع المودولات.
💾 تقارير فورية: يتم تصفية النتائج وحفظها تلقائياً في ملفات نصية مرتبة بصيغة .txt.
🚀 التثبيت والتشغيل
افتح تطبيق Termux أو مبادل أوامر نظام Linux، ثم قم بنسخ الأوامر التالية وتشغيلها بالترتيب:
git clone [https://github.com/ThT0AltayHR/Auto_Dork.git](https://github.com/ThT0AltayHR/Auto_Dork.git)
cd Auto_Dork
bash setup.sh
python dork_tool.py

📜 حقوق الملكية الفكرية والترخيص
⚠️ تحذير هام: يمنع نسخ أو إعادة إنتاج الأداة منعا باتاً.
هذا المشروع ومحتوياته البرمجية وهيكليته مسجل تحت الملكية الفكرية الخاصة بالمطور AltayHR. يمنع منعاً باتاً نسخ الأكواد، أو تعديلها، أو إعادة نشرها بأسماء أخرى، أو دمجها في مشاريع تجارية دون إذن خطي مسبق.
⚖️ إخلاء المسؤولية القانونية
تم تصميم هذه الأداة لأغراض اختبار الاختراق الأخلاقي المصرح به، والتحليلات الدفاعية والتعليمية فقط. لا يتحمل المطور (AltayHR) أو شبكة Turkhackteam أي مسؤولية مدنية أو جنائية عن إساءة استخدام هذه الأداة ضد أي أنظمة أو شبكات. المسؤولية الكاملة تقع على عاتق المستخدم.
