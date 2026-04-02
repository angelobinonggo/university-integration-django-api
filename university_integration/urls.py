"""
URL configuration for university_integration project.
Hub-and-Spoke Architecture:
  - /api/students/        -> Student App (spoke)
  - /api/library/         -> Library App (spoke)
  - /api/payments/        -> Payment App (spoke)
  - /api/hub/             -> Integration Hub (central hub)
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def index(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University Integration Platform</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container { max-width: 860px; margin: 0 auto; }
            header { text-align: center; margin-bottom: 48px; }
            header h1 {
                font-size: 2.2rem;
                font-weight: 700;
                background: linear-gradient(135deg, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 8px;
            }
            header p { color: #94a3b8; font-size: 1rem; }
            .badge {
                display: inline-block;
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 20px;
                padding: 4px 14px;
                font-size: 0.78rem;
                color: #38bdf8;
                margin-top: 12px;
            }
            .section { margin-bottom: 36px; }
            .section-title {
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: #64748b;
                margin-bottom: 12px;
                padding-bottom: 8px;
                border-bottom: 1px solid #1e293b;
            }
            .card {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                overflow: hidden;
                margin-bottom: 10px;
                transition: border-color 0.2s;
            }
            .card:hover { border-color: #38bdf8; }
            .card a {
                display: flex;
                align-items: center;
                gap: 14px;
                padding: 14px 18px;
                text-decoration: none;
                color: inherit;
            }
            .method {
                font-size: 0.68rem;
                font-weight: 700;
                width: 42px;
                text-align: center;
                padding: 3px 0;
                border-radius: 5px;
                flex-shrink: 0;
            }
            .get { background: #052e16; color: #4ade80; }
            .post { background: #1e1b4b; color: #818cf8; }
            .endpoint { font-size: 0.88rem; font-family: monospace; color: #7dd3fc; flex: 1; }
            .desc { font-size: 0.8rem; color: #64748b; }
            .spoke-label {
                font-size: 0.7rem;
                padding: 2px 10px;
                border-radius: 20px;
                font-weight: 600;
                flex-shrink: 0;
            }
            .hub-badge { background: #450a0a; color: #f87171; }
            .student-badge { background: #0c1a2e; color: #38bdf8; }
            .library-badge { background: #052e16; color: #4ade80; }
            .payment-badge { background: #2d1a00; color: #fb923c; }
            footer {
                text-align: center;
                margin-top: 60px;
                color: #334155;
                font-size: 0.78rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>University Integration Platform</h1>
                <p>Hub-and-Spoke REST API · IT322 Integrative Programming</p>
                <span class="badge">Django REST Framework · Hub-and-Spoke Architecture</span>
            </header>

            <div class="section">
                <div class="section-title">🔴 Integration Hub (Central Hub)</div>
                <div class="card"><a href="/api/hub/health/" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/hub/health/</span>
                    <span class="desc">System health — all spoke status</span>
                    <span class="spoke-label hub-badge">HUB</span>
                </a></div>
                <div class="card"><a href="/api/hub/student-summary/?student_id=S001" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/hub/student-summary/?student_id=S001</span>
                    <span class="desc">Unified student report (Request-Response + Transformation)</span>
                    <span class="spoke-label hub-badge">HUB</span>
                </a></div>
                <div class="card"><a href="/api/hub/all-summaries/" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/hub/all-summaries/</span>
                    <span class="desc">All student summaries (Aggregator pattern)</span>
                    <span class="spoke-label hub-badge">HUB</span>
                </a></div>
            </div>

            <div class="section">
                <div class="section-title">🔵 Student App (Spoke 1)</div>
                <div class="card"><a href="/api/students/" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/students/</span>
                    <span class="desc">List all students</span>
                    <span class="spoke-label student-badge">STUDENT</span>
                </a></div>
                <div class="card"><a href="/api/students/by_student_id/?student_id=S001" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/students/by_student_id/?student_id=S001</span>
                    <span class="desc">Lookup student by student_id</span>
                    <span class="spoke-label student-badge">STUDENT</span>
                </a></div>
            </div>

            <div class="section">
                <div class="section-title">🟢 Library App (Spoke 2)</div>
                <div class="card"><a href="/api/library/" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/library/</span>
                    <span class="desc">List all library records</span>
                    <span class="spoke-label library-badge">LIBRARY</span>
                </a></div>
                <div class="card"><a href="/api/library/by_student_id/?student_id=S001" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/library/by_student_id/?student_id=S001</span>
                    <span class="desc">Lookup library record by student_id</span>
                    <span class="spoke-label library-badge">LIBRARY</span>
                </a></div>
            </div>

            <div class="section">
                <div class="section-title">🟡 Payment App (Spoke 3)</div>
                <div class="card"><a href="/api/payments/" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/payments/</span>
                    <span class="desc">List all payment records</span>
                    <span class="spoke-label payment-badge">PAYMENT</span>
                </a></div>
                <div class="card"><a href="/api/payments/by_student_id/?student_id=S001" target="_blank">
                    <span class="method get">GET</span>
                    <span class="endpoint">/api/payments/by_student_id/?student_id=S001</span>
                    <span class="desc">Payment history by student_id</span>
                    <span class="spoke-label payment-badge">PAYMENT</span>
                </a></div>
            </div>

            <footer>IT322 &mdash; Integrative Programming &nbsp;|&nbsp; Lab Activity Module 1</footer>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('student_app.urls')),
    path('api/', include('library_app.urls')),
    path('api/', include('payment_app.urls')),
    path('api/', include('integration_hub.urls')),
]
