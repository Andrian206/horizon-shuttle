horizon-shuttle/
│
├── .env                          # API keys + hardcode login
├── requirements.txt              # 6 dependencies saja
├── main.py                       # SATU file backend (±100 baris)
│
├── static/
│   ├── index.html               # Landing page (dari Figma/Stitch)
│   ├── chat.html                # Horizon AI Public
│   ├── login.html               # Login hardcode
│   ├── workspace.html           # Horizon AI Workspace (3 mode)
│   ├── css/style.css            # Override (kalau perlu)
│   └── js/
│       ├── chat.js              # Public chat logic
│       ├── workspace.js         # Workspace chat logic
│       └── auth.js              # JWT check + logout
│
└── data/                         # 12 file knowledge base
    ├── 01_company_profile.txt
    ├── 02_service_catalog.txt
    ├── 03_route_schedule.txt
    ├── 04_fleet_info.txt
    ├── 05_faq.txt
    ├── 06_company_policies.txt
    ├── 07_cs_sop.txt
    ├── 08_marketing_guideline.txt
    ├── 09_promotional_campaign.txt
    ├── 10_business_reports.txt
    ├── 11_customer_reviews.txt
    └── 12_internal_sop.txt