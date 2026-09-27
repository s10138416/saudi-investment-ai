# Architecture v0.1.0

## Principle
The frontend displays results. The backend owns secrets, data normalization, calculations, scoring and decisions.

## Pipeline
SAHMK Pro -> FastAPI -> normalization -> financial/fundamental engines -> valuation -> liquidity/order flow -> risk -> decision -> Flutter.

## Safety / reliability rules
1. Never put SAHMK keys in Flutter.
2. Missing data stays null; never silently convert missing values to zero.
3. Every calculated metric should eventually carry source date/provenance.
4. AI must not invent financial numbers.
5. 'Institutional accumulation' must not be asserted from CMF/OBV alone.
6. No final BUY/SELL engine until the rules are backtested and walk-forward tested.
