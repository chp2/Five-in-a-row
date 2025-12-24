# ⚫ Omok-Lab: AI-Powered Gomoku Analysis Tool

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt-6.0-41CD52?style=flat-square&logo=qt&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24-013243?style=flat-square&logo=numpy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

> **"오목의 신의 한 수를 찾아서"**
>
> **Omok-Lab**은 렌주룰(Renju Rule)을 완벽하게 지원하는 오목 게임이자, 실시간 AI 분석 도구입니다.
> Minimax 알고리즘을 통해 플레이어의 다음 수를 예측하고, 승률 그래프와 훈수(Coaching) 기능을 통해 전략적인 플레이를 돕습니다.

---

## 🖥️ Screen Shot
*(여기에 실제 실행 화면 스크린샷이나 GIF를 넣으세요)*
![App Screenshot](./assets/screenshot_main.png)

---

## 🚀 Key Features

### 1. Renju Rule Implementation (렌주룰 엔진)
* 일반적인 오목(Gomoku)과 달리, 흑돌에게 불리함을 주는 **국제 룰(Renju)**을 로직으로 구현했습니다.
* **금지수 탐지:** 3-3, 4-4, 장목(6목 이상) 지점을 실시간으로 계산하여 착수를 방지하고 시각적으로 표시(Red X)합니다.

### 2. AI Analysis & Coaching (실시간 분석)
* **Minimax Algorithm:** Alpha-Beta Pruning(가지치기) 기법을 적용하여 3~4수 앞을 내다보는 최적의 수를 추천합니다.
* **Win Probability Graph:** 현재 바둑판의 형세를 분석하여 흑/백 승률 추이를 실시간 그래프로 시각화했습니다.

### 3. Professional GUI
* **PyQt6**를 활용하여 시스템 OS에 종속되지 않는 깔끔한 데스크톱 앱을 구축했습니다.
* 장시간 플레이에도 눈이 편안한 **Dark Mode**와 직관적인 UX를 제공합니다.

---

## 🛠️ Tech Stack & Architecture

이 프로젝트는 **MVC (Model-View-Controller)** 패턴을 엄격하게 준수하여 설계되었습니다.

* **Model (`core/`):** 오목판의 상태(`board`), 룰 판정(`rule_engine`), AI 알고리즘(`minimax`) 등 순수 로직을 담당합니다. UI 라이브러리에 의존하지 않아 테스트가 용이합니다.
* **View (`ui/`):** `PyQt6`를 사용하여 오목판을 그리고(`Painter`), 사용자 입력을 받습니다. Model의 상태 변화를 시각화합니다.
* **Controller (`main.py`):** 사용자의 입력(Click)을 받아 Model을 업데이트하고, AI 스레드를 관리하며 View를 갱신합니다.

| Category | Tech |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **GUI Framework** | PyQt6 |
| **Logic/Calculation** | NumPy (Matrix Operation) |
| **Design Resource** | Stitch AI (UI Concept) |

---

## 🔥 Technical Challenges (트러블 슈팅)

### Q. AI가 수를 생각할 때 화면이 멈추는 현상 (Freezing)
* **Problem:** Minimax 알고리즘이 재귀적으로 수만 가지 경우의 수를 계산하는 동안 메인 UI 스레드가 블로킹되어 프로그램이 '응답 없음' 상태가 됨.
* **Solution:** **`QThread`와 `pyqtSignal`을 도입**하여 AI 연산을 백그라운드 워커 스레드로 분리. 계산이 완료되면 시그널을 통해 메인 스레드에 좌표만 전달하도록 개선하여 UI 반응성을 확보함.

### Q. 렌주룰(3-3 금지) 알고리즘의 복잡성
* **Problem:** 단순히 '3개가 연속됨'을 찾는 것이 아니라, '열린 3(Open 3)'과 '닫힌 3'을 구분하고, 두 개의 3이 동시에 만들어지는지 판별해야 함.
* **Solution:** 방향 벡터(가로, 세로, 대각선)를 활용한 패턴 매칭 함수를 작성하고, 착수 시점 기준으로 4방향을 스캔하여 금지수 여부를 `O(1)`에 가깝게 판단하도록 최적화.

---

## 🏃 How to Run

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_GITHUB_ID/Omok-Lab.git](https://github.com/YOUR_GITHUB_ID/Omok-Lab.git)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python main.py