# Product Requirements Document (PRD)
# Omok-Lab: AI-Powered Gomoku Analysis Tool

**Version:** 2.4.0 (Pro)  
**Last Updated:** 2025-12-24  
**Document Owner:** Development Team  
**Status:** In Development

---

## 📋 Executive Summary

**Omok-Lab**은 렌주룰(Renju Rule)을 완벽하게 지원하는 오목 게임이자, 실시간 AI 분석 도구입니다. 플레이어가 전략적으로 더 나은 수를 두도록 돕는 AI 코칭 시스템을 제공하며, "오목의 신의 한 수를 찾아서"라는 비전 아래 개발됩니다.

### Target Users
- 오목 초보자부터 고급 플레이어까지
- 렌주룰을 학습하고자 하는 사용자
- AI 분석을 통해 전략을 개선하고자 하는 플레이어
- 오목 교육자 및 코치

---

## 🎯 Product Vision & Goals

### Vision Statement
> "모든 오목 플레이어가 AI의 도움으로 전략적 사고를 키우고, 렌주룰의 깊이를 이해하며, 최고의 한 수를 찾을 수 있도록 돕는다."

### Primary Goals
1. **렌주룰 완벽 구현**: 국제 표준 렌주룰(3-3, 4-4, 장목 금지)을 정확하게 구현
2. **실시간 AI 분석**: Minimax 알고리즘을 통한 최적의 수 추천 및 형세 분석
3. **직관적인 UX**: 전문가와 초보자 모두가 쉽게 사용할 수 있는 인터페이스
4. **교육적 가치**: 플레이어가 왜 특정 수가 좋은지 이해할 수 있도록 설명 제공

---

## 🖥️ User Interface Specification

### 1. Application Layout

#### 1.1 Header Bar
**Component:** Top Navigation Bar
- **Logo & Title**: 
  - Grid icon (Material Symbol: `grid_on`)
  - "Omok-Lab" 타이틀 (Bold, 18px)
  - 버전 정보 "v2.4.0 (Pro)" (12px, gray)
- **Window Controls**:
  - Minimize, Maximize, Close buttons
  - Hover effect: background color change
- **User Profile**:
  - Circular avatar (32px)
  - Ring border for visual emphasis
- **Styling**:
  - Background: `#111418`
  - Border bottom: `#283039`
  - Height: ~48px
  - z-index: 50 (always on top)

#### 1.2 Main Game Board (Left Panel)
**Component:** Interactive Omok Board

**Board Specifications:**
- **Grid Size**: 15x15
- **Board Style**:
  - Background: Wood texture (`#eab676`)
  - Border: 12px solid `#cca372` (frame effect)
  - Rounded corners: 2px
  - Shadow: Large drop shadow for depth
  - Aspect ratio: Square (1:1)
  - Max height: 800px
  - Responsive: `calc(100vh - 160px)`

**Grid Lines:**
- Color: `rgba(0,0,0,0.4)`
- Width: 1px
- Style: Solid lines crossing at intersections

**Star Points (Hoshi):**
- Position: (3,3), (3,11), (7,7), (11,3), (11,11) - 0-indexed
- Style: Small black dot (4px diameter)
- Purpose: Visual reference points

**Stone Rendering:**
- **Black Stone**:
  - Color: `#1e293b` (slate-900)
  - Size: 85% of cell size
  - Shadow: `shadow-md shadow-black/40`
  - Gradient highlight: Top-left corner for 3D effect
- **White Stone**:
  - Color: `#f1f5f9` (slate-100)
  - Border: 1px `#cbd5e1` (slate-300)
  - Size: 85% of cell size
  - Shadow: `shadow-md shadow-black/30`

**Move Number Display:**
- Position: Bottom-right of stone
- Style: Red badge with white text
- Font size: 10px
- Background: `#ef4444`
- Padding: 2px 4px
- Border radius: 2px

**Special Indicators:**
- **AI Recommended Move**:
  - Green pulsing circle (50% of cell size)
  - Color: `#22c55e` with 60% opacity
  - Ring: 2px `#4ade80`
  - Animation: Pulse effect
- **Forbidden Move (금지수)**:
  - Red X icon (Material Symbol: `close`)
  - Color: `#dc2626`
  - Size: 32px
  - Font weight: Bold

**Hover Effects:**
- Cell hover: Subtle background darkening
- Cursor: Pointer on empty cells

#### 1.3 Floating Toolbar
**Component:** Action Buttons

**Position:** Bottom center of board area
- Transform: Translate down with margin-top: 16px

**Buttons:**
1. **Undo** (`undo` icon)
2. **Redo** (`redo` icon)
3. **Divider**
4. **Flip Board** (`cached` icon)
5. **Toggle Coordinates** (`123` icon)
6. **Divider**
7. **Settings** (`settings` icon)

**Styling:**
- Background: `#1c2127/90` with backdrop blur
- Border: 1px `#283039`
- Border radius: Full (pill shape)
- Padding: 8px 24px
- Shadow: Large shadow for elevation
- Icon color: `white/70` → `white` on hover
- Transition: All 200ms

#### 1.4 Right Sidebar (Analysis Panel)
**Component:** Multi-section Analysis Dashboard
**Width:** 420px (fixed)
**Background:** `#111418`
**Border:** Left border `#283039`

##### Section 1: Win Probability Chart (Top)
**Background:** `#161b22`
**Padding:** 20px
**Border bottom:** `#283039`

**Header:**
- Title: "Win Probability" (14px, `#9dabb9`)
- Current Win Rate: Large bold number (36px) + player color
  - Example: "65% Black"
- Trend Indicator:
  - Icon: `trending_up` or `trending_down`
  - Color: Green for positive, Red for negative
  - Text: "+12%" or "-8%"
- Move Counter: "Move 45" (12px, top-right)
- Status Badge: "Thinking..." (Blue badge with border)

**Chart Visualization:**
- Type: Area chart with gradient fill
- Height: 128px
- Grid: 3 horizontal dashed lines (`#283039`)
- Line color: `#2b8cee` (primary blue)
- Fill: Gradient from `#2b8cee/30` to transparent
- Current point: White dot with blue ring
- X-axis: Move progression (implicit)
- Y-axis: Win probability 0-100%

##### Section 2: Move History (Middle - Scrollable)
**Background:** `#111418`
**Flex:** 1 (takes remaining space)

**Sub-header:**
- Title: "Move History" (14px, semibold)
- Action buttons:
  - Download icon (`download`)
  - Share icon (`ios_share`)
  - Hover: `#283039` background

**Table:**
- **Columns:**
  1. `#` - Move number (16px width)
  2. `Black` - Black's move in coordinate notation
  3. `White` - White's move in coordinate notation
  4. `Time` - Time taken for move (right-aligned)

- **Header Row:**
  - Background: `#1c2127`
  - Text: 12px uppercase, `#9dabb9`
  - Sticky position (stays on top when scrolling)

- **Data Rows:**
  - Font: Monospace for coordinates
  - Hover: `#1c2127` background
  - Divider: 1px `#283039`
  - Empty moves: "--" in gray

- **Current Move Highlight:**
  - Background: `#2b8cee/10` (primary with opacity)
  - Left border: 2px `#2b8cee`
  - Text color: `#2b8cee`
  - Font weight: Bold
  - Label: "Now" instead of time

**Scrolling:**
- Overflow-y: Auto
- Scrollbar: Hidden (custom styling)
- Smooth scroll behavior

##### Section 3: AI Analysis Chat (Bottom)
**Background:** `#161b22`
**Padding:** 16px 16px 24px
**Border top:** `#283039`

**AI Avatar:**
- Size: 40px circular
- Gradient ring: Indigo → Purple → Pink (2px)
- Inner background: Black
- Image: AI robot avatar
- Status indicator: Green dot (12px) bottom-right

**Chat Bubble:**
- Background: `#1c2127`
- Border: 1px `#283039`
- Border radius: 16px (rounded-tl-none for speech bubble effect)
- Padding: 12px
- Shadow: Small shadow

**Message Content:**
- Font size: 14px
- Line height: Relaxed
- Color: `#d1d5db` (gray-300)
- Highlights:
  - Move notation: Primary blue, semibold
  - Special terms (e.g., "San-San"): Yellow, medium weight

**Action Buttons:**
- Style: Small pills (12px text)
- Primary action: Blue background with 20% opacity
- Secondary action: Gray background `#283039`
- Hover: Increased opacity
- Padding: 4px 8px

**Input Field:**
- Width: 100%
- Background: `#111418`
- Border: 1px `#283039`
- Border radius: 8px
- Padding: 10px 40px 10px 16px
- Placeholder: "Ask AI about this position..."
- Focus state:
  - Border: `#2b8cee`
  - Ring: 1px `#2b8cee`
- Send button: Positioned absolute right
  - Icon: `send`
  - Hover: Primary blue color

**Metadata:**
- Name: "OmokBot AI" (14px, bold, white)
- Timestamp: "Just now" (10px, `#9dabb9`)

---

## 🎨 Design System

### Color Palette

#### Primary Colors
```
Primary Blue: #2b8cee
Background Dark: #101922
Surface Dark: #1c2127
Surface Darker: #111418
Border: #283039
Board Wood: #eab676
Board Frame: #cca372
```

#### Semantic Colors
```
Success/AI Recommendation: #22c55e
Warning/Special Term: #eab308
Error/Forbidden: #dc2626
Info/Thinking: #3b82f6
```

#### Text Colors
```
Primary Text: #ffffff
Secondary Text: #9dabb9
Tertiary Text: #6b7280
Disabled: #4b5563
```

### Typography

#### Font Families
- **Display/Headings:** Inter (Google Fonts)
- **Body/UI:** Noto Sans (Google Fonts)
- **Coordinates/Data:** Monospace (system)
- **Icons:** Material Symbols Outlined

#### Font Sizes
```
Title: 18px (bold)
Section Header: 14px (semibold)
Win Rate: 36px (bold)
Body: 14px (regular)
Small: 12px
Tiny: 10px
```

### Spacing Scale
```
xs: 4px
sm: 8px
md: 12px
lg: 16px
xl: 20px
2xl: 24px
3xl: 32px
```

### Border Radius
```
Default: 4px
Large: 8px
XL: 12px
2XL: 16px
Full: 9999px (pill/circle)
```

### Shadows
```
Small: 0 1px 2px rgba(0,0,0,0.05)
Medium: 0 4px 6px rgba(0,0,0,0.1)
Large: 0 10px 15px rgba(0,0,0,0.1)
XL: 0 20px 25px rgba(0,0,0,0.15)
```

---

## ⚙️ Functional Requirements

### FR-1: Game Board Management

#### FR-1.1: Board Initialization
- **Description:** 15x15 빈 오목판을 생성하고 초기화
- **Acceptance Criteria:**
  - 15x15 그리드가 정확하게 렌더링됨
  - 5개의 화점(star points)이 올바른 위치에 표시됨
  - 좌표 시스템이 정확함 (A-O, 1-15)
  - 모든 교차점이 클릭 가능함

#### FR-1.2: Stone Placement
- **Description:** 사용자가 빈 교차점을 클릭하여 돌을 놓을 수 있음
- **Acceptance Criteria:**
  - 빈 교차점만 클릭 가능
  - 흑돌과 백돌이 번갈아 가며 놓임
  - 돌이 놓인 후 시각적 피드백 제공
  - 돌 위에 수순 번호 표시
  - 금지수 위치는 착수 불가

#### FR-1.3: Move Validation
- **Description:** 렌주룰에 따라 착수의 유효성을 검증
- **Acceptance Criteria:**
  - 이미 돌이 있는 위치는 착수 불가
  - 흑돌의 3-3 금지 검증
  - 흑돌의 4-4 금지 검증
  - 흑돌의 장목(6목 이상) 금지 검증
  - 금지수 위치에 빨간 X 표시

### FR-2: Renju Rule Engine

#### FR-2.1: Forbidden Move Detection (3-3)
- **Description:** 흑돌이 동시에 두 개의 열린 3을 만드는 수를 탐지
- **Algorithm:**
  - 착수 후 4방향(가로, 세로, 대각선 2개) 스캔
  - 각 방향에서 "열린 3" 패턴 확인
  - 두 개 이상의 열린 3이 발견되면 금지수로 판정
- **Acceptance Criteria:**
  - 열린 3과 닫힌 3을 정확히 구분
  - 모든 3-3 금지 패턴을 탐지
  - 실시간으로 금지수 위치 표시

#### FR-2.2: Forbidden Move Detection (4-4)
- **Description:** 흑돌이 동시에 두 개의 열린 4를 만드는 수를 탐지
- **Algorithm:**
  - 착수 후 4방향 스캔
  - 각 방향에서 "열린 4" 패턴 확인
  - 두 개 이상의 열린 4가 발견되면 금지수로 판정
- **Acceptance Criteria:**
  - 열린 4와 닫힌 4를 정확히 구분
  - 모든 4-4 금지 패턴을 탐지
  - 실시간으로 금지수 위치 표시

#### FR-2.3: Forbidden Move Detection (Overline)
- **Description:** 흑돌이 6개 이상 연속으로 놓는 수를 탐지
- **Algorithm:**
  - 착수 후 4방향 스캔
  - 연속된 흑돌 개수 카운트
  - 6개 이상이면 금지수로 판정
- **Acceptance Criteria:**
  - 정확히 6개 이상만 금지수로 판정
  - 5목은 승리로 인정
  - 실시간으로 금지수 위치 표시

#### FR-2.4: Win Condition Detection
- **Description:** 5목이 완성되었는지 확인
- **Acceptance Criteria:**
  - 가로, 세로, 대각선 모든 방향 확인
  - 정확히 5개 연속 또는 5개 이상(백돌만)
  - 승리 시 게임 종료 및 알림
  - 승리한 5목 라인 하이라이트

### FR-3: AI Analysis Engine

#### FR-3.1: Minimax Algorithm Implementation
- **Description:** Alpha-Beta Pruning을 적용한 Minimax 알고리즘
- **Specifications:**
  - Search depth: 3-4 levels (configurable)
  - Evaluation function: 패턴 기반 점수 계산
  - Pruning: Alpha-Beta 가지치기
  - Time limit: 5초 (configurable)
- **Acceptance Criteria:**
  - 3초 이내에 최적의 수 추천
  - 승률 계산 정확도 ±5% 이내
  - UI 블로킹 없이 백그라운드 실행

#### FR-3.2: Position Evaluation
- **Description:** 현재 바둑판 형세를 평가하여 점수 산출
- **Evaluation Factors:**
  - 5목: +100000 (즉시 승리)
  - 열린 4: +10000
  - 닫힌 4: +1000
  - 열린 3: +500
  - 닫힌 3: +100
  - 열린 2: +50
  - 중앙 위치 보너스
  - 연결성 보너스
- **Acceptance Criteria:**
  - 일관된 평가 결과
  - 대칭 위치는 동일한 점수
  - 렌주룰 금지수 페널티 적용

#### FR-3.3: Best Move Recommendation
- **Description:** AI가 추천하는 최선의 수를 시각적으로 표시
- **Acceptance Criteria:**
  - 초록색 펄스 애니메이션으로 표시
  - 추천 이유를 텍스트로 설명
  - 여러 후보수가 있을 경우 상위 3개 표시 (선택사항)
  - 사용자가 추천수를 무시하고 다른 수를 둘 수 있음

#### FR-3.4: Win Probability Calculation
- **Description:** 현재 형세에서 흑/백의 승률을 계산
- **Algorithm:**
  - Minimax 평가 점수를 0-100% 확률로 변환
  - Sigmoid 함수 또는 정규화 사용
  - 매 수마다 업데이트
- **Acceptance Criteria:**
  - 0-100% 범위 내 값
  - 흑 + 백 = 100%
  - 실시간 그래프 업데이트
  - 추세 표시 (상승/하락 %)

### FR-4: Win Probability Chart

#### FR-4.1: Real-time Chart Update
- **Description:** 매 수마다 승률 그래프를 업데이트
- **Acceptance Criteria:**
  - SVG 기반 부드러운 곡선
  - 애니메이션 전환 효과
  - 현재 수 위치에 점 표시
  - 그리드 라인 표시

#### FR-4.2: Historical Data Display
- **Description:** 게임 시작부터 현재까지의 승률 변화를 표시
- **Acceptance Criteria:**
  - X축: 수 진행 (1~현재)
  - Y축: 승률 (0-100%)
  - 영역 차트 (Area chart) 스타일
  - 그라데이션 fill 효과

### FR-5: Move History

#### FR-5.1: Move Recording
- **Description:** 모든 착수를 순서대로 기록
- **Data Structure:**
  ```
  {
    moveNumber: number,
    player: 'black' | 'white',
    coordinate: string, // e.g., "H8"
    timestamp: number,
    timeTaken: number, // seconds
  }
  ```
- **Acceptance Criteria:**
  - 모든 착수가 순서대로 기록됨
  - 좌표 표기법 정확 (A-O, 1-15)
  - 시간 정보 저장

#### FR-5.2: Move Navigation
- **Description:** 사용자가 기록된 수를 클릭하여 해당 시점으로 이동
- **Acceptance Criteria:**
  - 클릭한 수까지의 바둑판 상태 복원
  - 현재 수 하이라이트
  - 스크롤 자동 조정
  - Undo/Redo 버튼과 연동

#### FR-5.3: Export Move History
- **Description:** 기보를 파일로 저장
- **Formats:**
  - SGF (Smart Game Format)
  - JSON
  - Plain text
- **Acceptance Criteria:**
  - 다운로드 버튼 클릭 시 파일 저장
  - 모든 메타데이터 포함 (날짜, 플레이어, 결과 등)
  - 다시 불러오기 가능

### FR-6: AI Chat Interface

#### FR-6.1: Contextual Analysis
- **Description:** 현재 수에 대한 AI의 분석을 자연어로 제공
- **Analysis Content:**
  - 현재 수의 의도 설명
  - 위협 요소 식별
  - 다음 예상 수 제안
  - 전략적 조언
- **Acceptance Criteria:**
  - 매 수마다 자동 분석 메시지 생성
  - 중요 용어 하이라이트 (색상 구분)
  - 읽기 쉬운 자연어 문장

#### FR-6.2: Interactive Q&A
- **Description:** 사용자가 AI에게 질문할 수 있는 입력창
- **Example Questions:**
  - "왜 이 수가 좋은가요?"
  - "다른 선택지는 무엇인가요?"
  - "이 위치는 금지수인가요?"
- **Acceptance Criteria:**
  - 텍스트 입력 필드
  - Enter 키 또는 전송 버튼으로 전송
  - AI 응답 생성 (로딩 상태 표시)
  - 대화 히스토리 유지

#### FR-6.3: Variation Display
- **Description:** "Show Variations" 버튼 클릭 시 다른 가능한 수순 표시
- **Acceptance Criteria:**
  - 상위 3개 변화도 표시
  - 각 변화도의 평가 점수 표시
  - 바둑판에 시각적으로 표시 (선택사항)

### FR-7: Board Controls

#### FR-7.1: Undo/Redo
- **Description:** 착수를 취소하거나 다시 실행
- **Acceptance Criteria:**
  - Undo: 마지막 수 제거
  - Redo: 취소한 수 복원
  - 단축키 지원 (Ctrl+Z, Ctrl+Y)
  - 버튼 활성화/비활성화 상태 관리

#### FR-7.2: Flip Board
- **Description:** 바둑판을 180도 회전
- **Acceptance Criteria:**
  - 애니메이션 효과
  - 좌표 레이블도 함께 회전
  - 돌의 위치는 유지

#### FR-7.3: Toggle Coordinates
- **Description:** 좌표 표시/숨김 전환
- **Acceptance Criteria:**
  - 버튼 클릭 시 토글
  - 상태 저장 (localStorage)
  - 부드러운 전환 효과

#### FR-7.4: Settings
- **Description:** 설정 모달 열기
- **Settings Options:**
  - AI 난이도 (탐색 깊이)
  - 시간 제한
  - 사운드 효과
  - 테마 (다크/라이트)
  - 좌표 표기법 (알파벳/숫자)
- **Acceptance Criteria:**
  - 모달 다이얼로그 표시
  - 설정 변경 즉시 적용
  - 설정 저장 (localStorage)

### FR-8: Performance Optimization

#### FR-8.1: Asynchronous AI Computation
- **Description:** AI 연산을 백그라운드 스레드에서 실행
- **Implementation:**
  - PyQt6 QThread 사용
  - pyqtSignal로 결과 전달
  - 진행 상태 표시 ("Thinking..." 배지)
- **Acceptance Criteria:**
  - UI 블로킹 없음
  - 연산 중 사용자 입력 가능
  - 취소 기능 제공

#### FR-8.2: Efficient Rendering
- **Description:** 바둑판 렌더링 최적화
- **Techniques:**
  - 변경된 부분만 다시 그리기
  - 캐싱 활용
  - 레이어 분리 (그리드, 돌, 표시)
- **Acceptance Criteria:**
  - 60 FPS 유지
  - 메모리 사용량 < 200MB
  - 부드러운 애니메이션

---

## 🔧 Technical Requirements

### TR-1: Technology Stack

#### TR-1.1: Programming Language
- **Language:** Python 3.10+
- **Reason:** 
  - 빠른 프로토타이핑
  - 풍부한 라이브러리 생태계
  - NumPy를 통한 효율적인 행렬 연산

#### TR-1.2: GUI Framework
- **Framework:** PyQt6
- **Reason:**
  - 크로스 플랫폼 지원 (Windows, macOS, Linux)
  - 네이티브 성능
  - 풍부한 위젯 및 커스터마이징
  - QThread를 통한 멀티스레딩

#### TR-1.3: Dependencies
```
PyQt6 >= 6.0
numpy >= 1.24
matplotlib >= 3.7 (for chart rendering, optional)
```

### TR-2: Architecture

#### TR-2.1: MVC Pattern
- **Model (`core/`):**
  - `board.py`: 바둑판 상태 관리
  - `rule_engine.py`: 렌주룰 검증
  - `minimax.py`: AI 알고리즘
  - `evaluator.py`: 형세 평가
  - UI 라이브러리에 독립적

- **View (`ui/`):**
  - `main_window.py`: 메인 윈도우
  - `board_widget.py`: 바둑판 위젯
  - `sidebar_widget.py`: 분석 패널
  - `chart_widget.py`: 승률 그래프
  - Model의 상태를 시각화

- **Controller (`main.py`):**
  - 사용자 입력 처리
  - Model 업데이트
  - View 갱신
  - AI 스레드 관리

#### TR-2.2: Data Flow
```
User Click → Controller → Model (validate) → Model (update) → 
Controller → View (render) → AI Thread (analyze) → 
Controller → View (show recommendation)
```

### TR-3: Performance Requirements

#### TR-3.1: Response Time
- **UI Interaction:** < 16ms (60 FPS)
- **Move Validation:** < 10ms
- **AI Recommendation:** < 5 seconds
- **Chart Update:** < 50ms

#### TR-3.2: Resource Usage
- **Memory:** < 200MB
- **CPU:** < 50% (single core during AI computation)
- **Disk:** < 50MB (application size)

### TR-4: Compatibility

#### TR-4.1: Operating Systems
- Windows 10/11
- macOS 11+
- Linux (Ubuntu 20.04+)

#### TR-4.2: Screen Resolutions
- Minimum: 1280x720
- Recommended: 1920x1080
- Maximum: 4K (3840x2160)

---

## 🧪 Testing Requirements

### Test-1: Unit Tests

#### Test-1.1: Rule Engine Tests
- **Test Cases:**
  - 3-3 금지 탐지 (20+ 케이스)
  - 4-4 금지 탐지 (20+ 케이스)
  - 장목 금지 탐지 (10+ 케이스)
  - 5목 승리 탐지 (10+ 케이스)
  - Edge cases (보드 가장자리)
- **Coverage:** > 95%

#### Test-1.2: AI Algorithm Tests
- **Test Cases:**
  - Minimax 정확성 (known positions)
  - Alpha-Beta pruning 효율성
  - Evaluation function 일관성
  - Time limit 준수
- **Coverage:** > 90%

### Test-2: Integration Tests

#### Test-2.1: UI-Model Integration
- **Test Scenarios:**
  - 사용자 착수 → 바둑판 업데이트
  - AI 추천 → UI 표시
  - 승률 계산 → 차트 업데이트
  - 기보 저장 → 불러오기

### Test-3: User Acceptance Tests

#### Test-3.1: Usability Testing
- **Participants:** 5-10 users (초보자 + 고급자)
- **Tasks:**
  1. 게임 시작 및 첫 수 놓기
  2. AI 추천 확인 및 따르기
  3. 금지수 위치 확인
  4. 기보 저장 및 불러오기
  5. 설정 변경
- **Success Criteria:** 80% 이상 작업 완료

---

## 📅 Development Roadmap

### Phase 1: Core Game Engine (Week 1-2)
- [ ] Board state management
- [ ] Stone placement logic
- [ ] Renju rule engine (3-3, 4-4, overline)
- [ ] Win condition detection
- [ ] Unit tests for rule engine

### Phase 2: Basic UI (Week 3-4)
- [ ] PyQt6 main window setup
- [ ] Board rendering (grid, stones)
- [ ] Click event handling
- [ ] Undo/Redo functionality
- [ ] Basic styling (dark theme)

### Phase 3: AI Engine (Week 5-6)
- [ ] Minimax algorithm implementation
- [ ] Alpha-Beta pruning
- [ ] Position evaluation function
- [ ] QThread integration
- [ ] Best move recommendation

### Phase 4: Analysis Features (Week 7-8)
- [ ] Win probability calculation
- [ ] Chart widget (SVG rendering)
- [ ] Move history table
- [ ] AI chat interface (basic)
- [ ] Export/Import SGF

### Phase 5: Polish & Optimization (Week 9-10)
- [ ] UI refinements (animations, transitions)
- [ ] Performance optimization
- [ ] Settings dialog
- [ ] Comprehensive testing
- [ ] Bug fixes

### Phase 6: Advanced Features (Week 11-12)
- [ ] Variation display
- [ ] Interactive Q&A with AI
- [ ] Advanced chart features
- [ ] Localization (Korean/English)
- [ ] User documentation

---

## 🎓 User Stories

### US-1: As a beginner player
> "나는 오목 초보자로서, 어떤 수가 금지수인지 실시간으로 알고 싶다."
- **Acceptance Criteria:**
  - 금지수 위치에 빨간 X 표시
  - 금지수를 클릭하면 경고 메시지
  - AI가 금지수 이유를 설명

### US-2: As an intermediate player
> "나는 중급 플레이어로서, AI가 추천하는 수를 보고 내 전략을 개선하고 싶다."
- **Acceptance Criteria:**
  - AI 추천 수가 초록색으로 표시됨
  - 추천 이유가 채팅창에 표시됨
  - 다른 후보수도 확인 가능

### US-3: As an advanced player
> "나는 고급 플레이어로서, 형세 변화를 그래프로 보고 싶다."
- **Acceptance Criteria:**
  - 승률 그래프가 실시간 업데이트됨
  - 특정 수를 클릭하면 그 시점의 형세 확인 가능
  - 변화도 분석 기능

### US-4: As a coach
> "나는 오목 코치로서, 학생들에게 보여줄 기보를 저장하고 공유하고 싶다."
- **Acceptance Criteria:**
  - SGF 형식으로 저장
  - 다른 프로그램에서도 열 수 있음
  - 주석 추가 가능

---

## 🚨 Risk Management

### Risk-1: AI Performance
- **Risk:** Minimax 알고리즘이 너무 느려서 UX 저하
- **Mitigation:**
  - Alpha-Beta pruning 최적화
  - 탐색 깊이 제한
  - 시간 제한 설정
  - Iterative deepening 적용

### Risk-2: Rule Complexity
- **Risk:** 렌주룰 구현의 복잡성으로 인한 버그
- **Mitigation:**
  - 철저한 단위 테스트
  - 알려진 금지수 패턴 데이터베이스 구축
  - 전문가 검증

### Risk-3: Cross-platform Issues
- **Risk:** PyQt6가 특정 OS에서 제대로 작동하지 않음
- **Mitigation:**
  - 각 OS에서 정기적 테스트
  - CI/CD 파이프라인 구축
  - 플랫폼별 빌드 스크립트

---

## 📊 Success Metrics

### Metric-1: User Engagement
- **Target:** 평균 세션 시간 > 20분
- **Measurement:** 앱 사용 시간 로깅

### Metric-2: AI Accuracy
- **Target:** 추천 수가 실제 최선의 수일 확률 > 80%
- **Measurement:** 전문가 평가, 기존 기보와 비교

### Metric-3: Performance
- **Target:** AI 응답 시간 < 3초 (95th percentile)
- **Measurement:** 성능 프로파일링

### Metric-4: User Satisfaction
- **Target:** 사용자 만족도 > 4.0/5.0
- **Measurement:** 사용자 설문조사

---

## 📝 Appendix

### A. Coordinate System
- **Columns:** A-O (15 letters, excluding I)
- **Rows:** 1-15 (bottom to top)
- **Example:** Center point = H8

### B. Renju Rule Reference
- **3-3 (San-San):** 흑이 동시에 두 개의 열린 3을 만드는 수
- **4-4 (Ssu-Ssu):** 흑이 동시에 두 개의 열린 4를 만드는 수
- **Overline (장목):** 흑이 6개 이상 연속으로 놓는 수
- **Open 3 (열린 3):** 양쪽이 막히지 않은 3
- **Open 4 (열린 4):** 양쪽이 막히지 않은 4

### C. SGF Format Example
```
(;FF[4]GM[11]SZ[15]
PB[Black Player]PW[White Player]
DT[2025-12-24]
;B[hh];W[hi];B[jj]
)
```

### D. Glossary
- **Hoshi (화점):** Star points on the board
- **Kifu (기보):** Game record
- **Tesuji (수근):** Clever move
- **Joseki (정석):** Standard opening sequence
- **Fuseki (포석):** Opening strategy

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-24 | Initial PRD based on UI design |

---

**Document Status:** ✅ Ready for Review  
**Next Review Date:** 2025-12-31  
**Approvers:** Product Manager, Tech Lead, UX Designer
