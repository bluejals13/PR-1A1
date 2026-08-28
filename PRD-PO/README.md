# PRD-PO: Portfolio & Presentation Repository

## 1. Overview & Responsibility
`PRD-PO/`는 `PR-Files/`에 축적된 엔지니어링 증거(Evidence)와 기술 명세를 기반으로, **외부 공개용 포트폴리오(Web/HTML), 12~15페이지 기술 발표자료(Presentation), 심층 기술 사례 연구(Case Study)**를 제작하는 공간입니다.

이 폴더의 문서는 **"Problem → Context → Decision → Implementation → Verification → Result → Limitation → Next Step"** 사고 흐름에 따라 고도로 정제되고 압축된 형태로 작성됩니다.

---

## 2. Directory Structure & Responsibilities

```
PRD-PO/
├── presentation/          # 면접/기술 발표용 12~15페이지 슬라이드 구성 및 원고
│   └── README.md
├── html/                  # Web 기반 인터랙티브 포트폴리오 웹 문서 및 에셋
│   └── README.md
├── case-study/            # 핵심 기술 난제 해결 심층 케이스 스터디 (Auth, Perf, TS)
│   └── README.md
└── README.md
```

---

## 3. Production Rules
1. **Evidence-Backed:** `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`에 등재되지 않은 가공 수치 및 미구현 기능 절대 작성 금지.
2. **Page Count Integrity:** 발표자료는 12~15페이지 내외로 제한하며, 각 슬라이드는 명확한 단 하나의 핵심 메시지(One Key Message)를 전달.
3. **Structured Flow:** 기술 나열을 지양하고, 어떤 문제를 해결하기 위해 어떤 의사결정을 내렸고 어떻게 검증했는지를 증명.
