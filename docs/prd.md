# Requirements Document

## 1. Application Overview

**Application Name**: AI-Powered Forex Signal Telegram Bot

**Description**: A production-ready Telegram bot providing AI-driven forex trading signals, market analysis, and portfolio management. All interactions occur within Telegram using inline keyboard navigation. The bot integrates multiple AI providers, supports premium subscriptions, and includes admin management capabilities.

---

## 2. Users and Use Scenarios

**Target Users**:
- Forex traders seeking AI-powered trading signals
- Users requiring real-time market analysis and news
- Premium subscribers accessing advanced features
- System administrators managing bot operations

**Core Use Scenarios**:
- Receive AI-generated forex signals with entry/exit points
- Access multi-timeframe technical analysis
- Monitor trading sessions and market volatility
- Subscribe to premium plans
- Track signal history and portfolio performance

---

## 3. Page Structure and Functional Description

### 3.1 Bot Menu Structure

```
Telegram Bot Interface
├── Start Menu
│   ├── Live Signals
│   ├── AI Analysis
│   ├── Market Scanner
│   ├── Trading Sessions
│   ├── Forex News
│   ├── Economic Calendar
│   ├── Portfolio
│   ├── Signal History
│   ├── Favorites
│   ├── Premium
│   ├── Profile
│   ├── Settings
│   └── Support
└── Admin Dashboard
    ├── Users Management
    ├── Revenue Analytics
    ├── Premium Management
    ├── Broadcast
    ├── Coupons
    ├── Payments
    ├── Signals Management
    ├── Logs
    ├── API Health
    ├── Restart Workers
    └── Backups
```

### 3.2 Functional Description

#### 3.2.1 Start Menu
- Display welcome message via Telegram message
- Show main navigation using inline keyboard buttons
- Include Home, Back, Refresh buttons for navigation

#### 3.2.2 Live Signals
- Display real-time forex signals in Telegram message format
- Show: currency pair, direction (BUY/SELL/NO TRADE), entry price, stop loss, TP1, TP2
- Display: confidence level, probability, risk score, risk/reward ratio, trade duration
- Include AI reasoning text
- Provide inline button to add signal to favorites
- Refresh button to generate new signal

#### 3.2.3 AI Analysis
- Select currency pair and timeframe via inline keyboard (M1, M5, M15, M30, H1, H4, D1)
- Display analysis results in Telegram message: trend, support/resistance, EMA 20/50/200, RSI, MACD, ADX, ATR, Bollinger Bands, VWAP, Stochastic, Fibonacci, market structure, liquidity zones, volume, breakout/retest patterns
- Show AI-generated explanations using Groq API and Google Gemini API

#### 3.2.4 Market Scanner
- Select timeframes and currency pairs via inline keyboard
- Display scan results in message format: signal strength, recommended actions
- Show multiple opportunities in single message or paginated messages

#### 3.2.5 Trading Sessions
- Display current active session (Sydney, Tokyo, London, New York) in message
- Show session overlap periods
- Use Africa/Addis_Ababa timezone (UTC+3)
- Highlight high-volatility periods

#### 3.2.6 Forex News
- Display latest forex news in message format
- Show sentiment analysis using Google Gemini API
- Filter news by currency via inline keyboard buttons

#### 3.2.7 Economic Calendar
- Display upcoming events in message format
- Show: event time, currency, importance level
- Provide AI interpretation using Google Gemini API

#### 3.2.8 Portfolio
- Display active and closed trades in message format
- Show: total profit/loss, win rate, average risk/reward
- List individual trade details

#### 3.2.9 Signal History
- Display past signals with outcomes in message format
- Filter by date range, currency pair, result via inline keyboard
- Show performance statistics

#### 3.2.10 Favorites
- Display saved signals and currency pairs in message format
- Add/remove favorites via inline buttons

#### 3.2.11 Premium
- Display subscription plans in message: Monthly, Quarterly, Yearly, Lifetime
- Show features and pricing
- Select payment method via inline keyboard: Stripe, PayPal, Telegram Stars, USDT, BTC, ETH
- Process payment and activate premium features

#### 3.2.12 Profile
- Display user information in message: username, subscription status, join date
- Show statistics: total signals received, trades tracked, premium expiry

#### 3.2.13 Settings
- Configure notification preferences via inline keyboard: new signals, TP/SL hits, high volatility alerts, major news
- Set preferred currency pairs and timeframes
- Adjust risk tolerance and signal filters

#### 3.2.14 Support
- Display contact information in message
- Show FAQ and educational resources
- Submit support requests via inline button

#### 3.2.15 Admin Dashboard
- **Users Management**: View user list, subscription status, activity logs in message format
- **Revenue Analytics**: Display revenue metrics, payment history, subscription trends
- **Premium Management**: Manage subscription plans, pricing, features via inline buttons
- **Broadcast**: Send messages to all users or specific segments
- **Coupons**: Create and manage discount coupons
- **Payments**: View payment transactions, process refunds
- **Signals Management**: Review generated signals, adjust parameters
- **Logs**: Access system logs, error reports, audit trails
- **API Health**: Monitor Groq API, Google Gemini API, market data providers status
- **Restart Workers**: Restart Celery workers and background tasks
- **Backups**: Trigger database backups, view backup history

---

## 4. Business Rules and Logic

### 4.1 Signal Generation Logic
- Analyze market data across M1, M5, M15, M30, H1, H4, D1 timeframes
- Calculate technical indicators: EMA 20/50/200, RSI, MACD, ADX, ATR, Bollinger Bands, VWAP, Stochastic, Fibonacci levels
- Identify trend direction, support/resistance zones, market structure, liquidity zones, volume patterns, breakout/retest scenarios
- Use Groq API for fast multi-timeframe analysis
- Use Google Gemini API for detailed reasoning
- Generate signal only when conditions meet predefined criteria
- Output BUY, SELL, or NO TRADE
- Calculate entry price, stop loss, TP1, TP2, confidence level, probability, risk score, risk/reward ratio, trade duration

### 4.2 Trading Session Detection
- Use Africa/Addis_Ababa timezone (UTC+3)
- Detect active sessions: Sydney, Tokyo, London, New York
- Identify session overlap periods
- Increase scan frequency during high-liquidity overlaps

### 4.3 Notification Rules
- Send Telegram notifications for: new signals, TP hit, SL hit, high volatility alerts, major news events
- Respect user notification preferences from Settings

### 4.4 Premium Subscription Logic
- Validate payment before activating premium features
- Support payment methods: Stripe, PayPal, Telegram Stars, USDT, BTC, ETH
- Apply subscription duration: Monthly, Quarterly, Yearly, Lifetime
- Automatically expire premium access when subscription ends
- Allow coupon codes for discounts

### 4.5 Market Data Provider Logic
- Support providers: TwelveData, Finnhub, Polygon, AlphaVantage, ForexRateAPI
- Fetch real-time and historical market data
- Handle provider API failures with fallback mechanisms

### 4.6 Security and Authentication
- Verify Telegram webhook signatures
- Implement role-based access control for admin features
- Apply rate limiting to prevent abuse
- Store API keys (GROQ_API_KEY, GEMINI_API_KEY) in environment variables only

### 4.7 Background Task Processing
- Use Celery for asynchronous tasks: signal generation, market scanning, notification delivery
- Schedule periodic tasks: session detection, news updates, economic calendar refresh
- Store task results in Redis for caching

---

## 5. Exception and Boundary Conditions

| Scenario | Handling |
|----------|----------|
| AI API failure (Groq or Gemini) | Log error, retry with exponential backoff, notify admin if persistent |
| Market data provider unavailable | Switch to fallback provider, log incident |
| Invalid user input | Display error message in Telegram, prompt correction |
| Payment processing failure | Notify user via Telegram message, log transaction, provide retry option |
| Database connection loss | Retry connection, queue operations, alert admin |
| Webhook verification failure | Reject request, log security event |
| Rate limit exceeded | Return rate limit error message, block requests temporarily |
| Signal generation timeout | Cancel task, log timeout, retry with adjusted parameters |
| Premium subscription expired | Disable premium features, notify user to renew |
| Admin command from non-admin user | Deny access, log unauthorized attempt |

---

## 6. Acceptance Criteria

1. User sends /start command and receives main menu with all navigation options displayed via inline keyboard buttons in Telegram
2. User selects Live Signals button and views AI-generated forex signal with entry, stop loss, TP1, TP2, confidence, probability, risk score, and detailed reasoning in Telegram message
3. User navigates to Premium menu via inline button, selects subscription plan, completes payment via Stripe, and premium features are activated
4. Admin sends /admin command, accesses admin dashboard via inline keyboard, and views user statistics, revenue analytics, and API health status in Telegram messages
5. System generates new signal during London-New York session overlap, sends Telegram notification to subscribed users, and logs signal in backend database

---

## 7. Out of Scope for This Release

- Automated trade execution on user's behalf
- Integration with broker APIs for direct trading
- Mobile app versions (iOS/Android native apps)
- Web dashboard interface outside Telegram
- Social trading features (copy trading, leaderboards)
- Multi-language support beyond English
- Voice/audio signal notifications
- Custom indicator creation by users
- Backtesting historical signals
- Live chat support within bot
- Referral program and affiliate system
- Advanced charting and visualization tools
- Integration with MetaTrader or other trading platforms
- Guaranteed profit promises or performance guarantees