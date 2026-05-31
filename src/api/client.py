"""
Zernio API Client - corregido con endpoints reales según docs.zernio.com
Base URL real: https://zernio.com/api/v1  (NO api.zernio.com)
"""

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class AuthError(Exception):
    pass


class AddonRequiredError(Exception):
    pass


# URL base correcta (confirmada en docs.zernio.com/platforms/instagram)
BASE_URL = "https://zernio.com/api/v1"


class ZernioClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ZERNIO_API_KEY")
        if not self.api_key:
            raise ValueError("ZERNIO_API_KEY debe estar en el constructor o como variable de entorno")

        self.account_id_instagram = os.getenv("ZERNIO_ACCOUNT_ID")
        self.account_id_youtube = os.getenv("ZERNIO_ACCOUNT_ID_YOUTUBE")

    def _request(self, method, path, params=None, data=None):
        url = f"{BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    timeout=30,
                )

                if response.status_code == 401:
                    raise AuthError("Autenticación fallida. Verifica tu API key.")
                if response.status_code in [402, 403]:
                    raise AddonRequiredError(f"Add-on requerido para: {path}")

                response.raise_for_status()
                return response.json()

            except (AuthError, AddonRequiredError):
                raise
            except requests.exceptions.HTTPError:
                raise
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Request fallido (intento {attempt + 1}), reintentando en {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e


    # Accounts
    # ─────────────────────────────────────────────

    def list_accounts(self):
        """GET /v1/accounts — lista todas las cuentas conectadas."""
        return self._request("GET", "/accounts")

    def get_follower_stats(self, account_id=None, platform="instagram"):
        """
        GET /v1/accounts/follower-stats
        Historial de seguidores de una cuenta.
        Docs: /analytics/get-analytics -> "For follower stats, use /v1/accounts/follower-stats"
        """
        account_id = account_id or self.account_id_instagram
        if not account_id:
            raise ValueError("account_id requerido")
        return self._request("GET", "/accounts/follower-stats", params={
            "accountId": account_id,
            "platform": platform,
        })

    # ─────────────────────────────────────────────
    # Analytics generales (post-level)
    # ─────────────────────────────────────────────

    def get_analytics(self, platform="instagram", account_id=None, from_date=None, to_date=None,
                      limit=50, page=1, sort_by="date", order="desc"):
        """
        GET /v1/analytics — analíticas de posts (paginado).
        Parámetros reales según docs.zernio.com/analytics/get-analytics
        """
        account_id = account_id or self.account_id_instagram
        params = {
            "platform": platform,
            "limit": limit,
            "page": page,
            "sortBy": sort_by,
            "order": order,
        }
        if account_id:
            params["accountId"] = account_id
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        return self._request("GET", "/analytics", params=params)

    # ─────────────────────────────────────────────
    # Analytics agregados (requieren Analytics add-on
    # según changelog de docs.zernio.com)
    # ─────────────────────────────────────────────

    def get_daily_metrics(self, platform="instagram", account_id=None, from_date=None, to_date=None):
        """
        GET /v1/analytics/daily-metrics
        Métricas diarias agregadas: impressions, reach, likes, comments, shares, saves, clicks, views.
        Filtros: platform, profileId, accountId, fromDate, toDate
        """
        account_id = account_id or self.account_id_instagram
        params = {"platform": platform}
        if account_id:
            params["accountId"] = account_id
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        return self._request("GET", "/analytics/daily-metrics", params=params)

    def get_best_time_to_post(self, platform="instagram", account_id=None):
        """
        GET /v1/analytics/best-time
        Slots agrupados por dayOfWeek (0=Lunes..6=Domingo) y hora (UTC 0-23) con avg_engagement.
        """
        account_id = account_id or self.account_id_instagram
        params = {"platform": platform}
        if account_id:
            params["accountId"] = account_id
        return self._request("GET", "/analytics/best-time", params=params)

    def get_content_decay(self, platform="instagram", account_id=None):
        """
        GET /v1/analytics/content-decay
        Buckets con bucketLabel y avgPctOfFinal (decaimiento del engagement con el tiempo).
        """
        account_id = account_id or self.account_id_instagram
        params = {"platform": platform}
        if account_id:
            params["accountId"] = account_id
        return self._request("GET", "/analytics/content-decay", params=params)

    def get_posting_frequency(self, platform="instagram", account_id=None):
        """
        GET /v1/analytics/posting-frequency
        Filas con postsPerWeek, avgEngagementRate, weeksCount.
        """
        account_id = account_id or self.account_id_instagram
        params = {"platform": platform}
        if account_id:
            params["accountId"] = account_id
        return self._request("GET", "/analytics/posting-frequency", params=params)

    # ─────────────────────────────────────────────
    # Analytics específicos de Instagram
    # ─────────────────────────────────────────────

    def get_instagram_account_insights(self, account_id=None, metrics=None,
                                        since=None, until=None,
                                        metric_type="timeseries"):
        """
        GET /v1/analytics/instagram/account-insights
        Rendimiento a nivel de cuenta (reach, impressions, etc.).
        - metricType: "timeseries" | "totalvalue"
        - Max rango: 90 días (por defecto últimos 30)
        - Puede tener delay de hasta 48h
        Requiere Analytics add-on.
        """
        account_id = account_id or self.account_id_instagram
        if not account_id:
            raise ValueError("account_id requerido")
        params = {
            "accountId": account_id,
            "metricType": metric_type,
        }
        if metrics:
            params["metrics"] = metrics  # lista o string separado por comas
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        return self._request("GET", "/analytics/instagram/account-insights", params=params)

    def get_demographics(self, account_id=None,
                          metric="followerDemographics",
                          breakdown="age",
                          timeframe="this_month"):
        """
        GET /v1/analytics/instagram/demographics
        Segmentación de audiencia.
        - metric: "followerDemographics" | "engagedAudienceDemographics"
        - breakdown: "age" | "city" | "country" | "gender"
        - timeframe: "thisWeek" | "this_month"
        Requiere 100+ seguidores. Puede tener delay de hasta 48h.
        Requiere Analytics add-on.
        """
        account_id = account_id or self.account_id_instagram
        if not account_id:
            raise ValueError("account_id requerido")
        return self._request("GET", "/analytics/instagram/demographics", params={
            "accountId": account_id,
            "metric": metric,
            "breakdown": breakdown,
            "timeframe": timeframe,
        })

    # Inbox
    # ─────────────────────────────────────────────

    def list_inbox_comments(self, account_id=None, platform="instagram"):
        """GET /v1/inbox/comments"""
        account_id = account_id or self.account_id_instagram
        params = {"platform": platform}
        if account_id:
            params["accountId"] = account_id
        return self._request("GET", "/inbox/comments", params=params)

    def list_conversations(self, account_id=None, platform="instagram"):
        """GET /v1/inbox/conversations"""
        account_id = account_id or self.account_id_instagram
        params = {"platform": platform}
        if account_id:
            params["accountId"] = account_id
        return self._request("GET", "/inbox/conversations", params=params)


    def validate_all_endpoints(self):
        """Valida todos los endpoints y reporta cuáles funcionan."""
        print("Validando endpoints de Zernio...")
        print("=" * 50)

        test_cases = [
            ("List Accounts",              lambda: self.list_accounts()),
            ("Post Analytics",             lambda: self.get_analytics()),
            ("Daily Metrics",              lambda: self.get_daily_metrics()),
            ("Best Time to Post",          lambda: self.get_best_time_to_post()),
            ("Content Decay",              lambda: self.get_content_decay()),
            ("Posting Frequency",          lambda: self.get_posting_frequency()),
            ("IG Account Insights",        lambda: self.get_instagram_account_insights()),
            ("IG Demographics",            lambda: self.get_demographics()),
            ("Follower Stats",             lambda: self.get_follower_stats()),
            ("Inbox Comments",             lambda: self.list_inbox_comments()),
            ("Inbox Conversations",        lambda: self.list_conversations()),
        ]

        results = {}
        for name, func in test_cases:
            try:
                result = func()
                results[name] = {"status": "SUCCESS", "result": result}
                print(f"✅ {name}: SUCCESS")
            except AuthError as e:
                results[name] = {"status": "AUTH_ERROR", "error": str(e)}
                print(f"❌ {name}: AUTH ERROR - {e}")
            except AddonRequiredError as e:
                results[name] = {"status": "ADDON_REQUIRED", "error": str(e)}
                print(f"⚠️  {name}: ADD-ON REQUERIDO - {e}")
            except Exception as e:
                results[name] = {"status": "ERROR", "error": str(e)}
                print(f"❌ {name}: ERROR - {e}")

        return results


if __name__ == "__main__":
    api_key = os.getenv("ZERNIO_API_KEY")
    account_id = os.getenv("ZERNIO_ACCOUNT_ID")

    if not api_key or not account_id:
        print("Falta ZERNIO_API_KEY o ZERNIO_ACCOUNT_ID en las variables de entorno")
        exit(1)

    client = ZernioClient(api_key=api_key)
    results = client.validate_all_endpoints()

    success_count = sum(1 for r in results.values() if r["status"] == "SUCCESS")
    print(f"\n📊 Resultado: {success_count}/{len(results)} endpoints funcionando")