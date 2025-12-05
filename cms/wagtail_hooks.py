"""
Hooks Wagtail pour personnaliser l'admin.
Interface professionnelle et dynamique avec prévisualisation responsive.
"""

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.models import Page, Site

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model


# =============================================================================
# CSS PERSONNALISÉ - THÈME PROFESSIONNEL HUBMAIRIE
# =============================================================================

@hooks.register("insert_global_admin_css")
def global_admin_css():
    return mark_safe(
        """
        <style>
            :root {
                --ecms-primary: #0C1E3C;
                --ecms-primary-light: #163A5F;
                --ecms-accent: #0066CC;
                --ecms-success: #059669;
                --ecms-warning: #D97706;
                --ecms-danger: #DC2626;
                --ecms-border: #E2E8F0;
                --ecms-surface: #F8FAFC;
                --ecms-text: #1E293B;
                --ecms-muted: #64748B;
            }

            .sidebar {background: linear-gradient(180deg, var(--ecms-primary), var(--ecms-primary-light)) !important;box-shadow: 4px 0 20px rgba(0,0,0,0.15);}
            header {background: white !important; border-bottom: 1px solid var(--ecms-border); box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
            .button, .button--primary {border-radius: 8px !important; font-weight: 500;}
            .button--primary {background: linear-gradient(135deg, var(--ecms-accent), #0052A3) !important;}

            .hubmairie-preview-btn {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.75rem 1.5rem;
                background: linear-gradient(135deg, #059669, #047857);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(5,150,105,0.3);
                text-decoration: none;
                transition: all 0.3s ease;
            }
            .hubmairie-preview-btn:hover {transform: translateY(-2px); box-shadow: 0 8px 25px rgba(5,150,105,0.4);}

            /* Modal de prévisualisation */
            .hubmairie-modal-overlay {
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(12,30,60,0.95); backdrop-filter: blur(10px);
                z-index: 10000; display: flex; align-items: center; justify-content: center;
                opacity: 0; visibility: hidden; transition: all 0.4s ease;
            }
            .hubmairie-modal-overlay.active {opacity: 1; visibility: visible;}
            .hubmairie-modal {
                background: white; width: 95vw; height: 90vh; max-width: 1400px;
                border-radius: 20px; overflow: hidden; box-shadow: 0 30px 100px rgba(0,0,0,0.6);
                display: flex; flex-direction: column; transform: scale(0.95); transition: transform 0.4s ease;
            }
            .hubmairie-modal-overlay.active .hubmairie-modal {transform: scale(1);}
            .hubmairie-modal-header {
                padding: 1rem 1.5rem; background: linear-gradient(135deg, var(--ecms-primary), var(--ecms-primary-light));
                color: white; display: flex; justify-content: space-between; align-items: center;
            }
            .hubmairie-modal-body {flex: 1; background: #0F172A; padding: 2rem; display: flex; justify-content: center; align-items: center;}

            /* Appareils */
            .hubmairie-desktop-frame {width: 100%; max-width: 1200px; height: 100%; background: #111; border-radius: 12px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.6);}
            .hubmairie-phone-frame {
                width: 375px; height: 812px; background: #000; border-radius: 55px; padding: 14px;
                box-shadow: 0 30px 80px rgba(0,0,0,0.8); position: relative; transform: scale(0.8);
            }
            .hubmairie-phone-frame::before {content: ''; position: absolute; top: 20px; left: 50%; transform: translateX(-50%); width: 130px; height: 34px; background: #000; border-radius: 20px;}
            .hubmairie-tablet-frame {
                width: 820px; height: 1100px; background: #000; border-radius: 40px; padding: 20px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.7); transform: scale(0.6);
            }
            .screen {width: 100%; height: 100%; background: white; border-radius: inherit; overflow: hidden;}
            iframe {width: 100%; height: 100%; border: none;}

            /* Boutons appareils */
            .hubmairie-device-btn {
                width: 44px; height: 44px; border-radius: 10px; background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2); color: white; cursor: pointer;
            }
            .hubmairie-device-btn.active {background: var(--ecms-accent); border-color: var(--ecms-accent);}
            .hubmairie-close-btn {background: rgba(220,38,38,0.8); margin-left: 1rem;}

            @media (max-width: 768px) {
                .hubmairie-modal {width: 100vw; height: 100vh; border-radius: 0;}
                .hubmairie-phone-frame {transform: scale(0.65);}
            }
        </style>
        """
    )


# =============================================================================
# JS + BOUTON PRÉVISUALISATION (CORRIGÉ ET ROBUSTE)
# =============================================================================

@hooks.register("insert_global_admin_js")
def global_admin_js():
    """
    Génère le bouton de prévisualisation avec gestion robuste des URLs.
    """
    try:
        site = Site.objects.get(is_default_site=True)
        homepage = site.root_page if site else None

        # Utilise l'URL de prévisualisation Wagtail pour éviter les erreurs de permission
        if homepage:
            preview_url = homepage.get_preview_url()
        else:
            preview_url = "http://localhost:8000/"
    except Exception as e:
        preview_url = "http://localhost:8000/"

    # Échappe l'URL correctement pour JavaScript
    preview_url_safe = preview_url.replace('"', '\\"').replace("'", "\\'")

    js_code = f"""
        <script>
            (function() {{
                const PREVIEW_URL = "{preview_url_safe}";
                
                document.addEventListener("DOMContentLoaded", function() {{
                    class PreviewModal {{
                        constructor() {{
                            this.current = "desktop";
                            this.url = PREVIEW_URL;
                            this.modal = null;
                            this.frameContainer = null;
                            this.init();
                        }}
                        
                        init() {{
                            this.createButton();
                            this.createModal();
                        }}
                        
                        createButton() {{
                            const selectors = [
                                ".w-slim-header__controls",
                                ".w-header-meta",
                                ".header-meta__actions",
                                "header"
                            ];
                            let container = null;
                            
                            for (const sel of selectors) {{
                                const el = document.querySelector(sel);
                                if (el) {{
                                    container = el;
                                    break;
                                }}
                            }}
                            
                            if (!container) container = document.body;
                            
                            const btn = document.createElement("a");
                            btn.href = "#";
                            btn.className = "hubmairie-preview-btn";
                            btn.style.cssText = "display:inline-flex;align-items:center;gap:0.5rem;padding:0.75rem 1.5rem;background:linear-gradient(135deg,#059669,#047857);color:white;border:none;border-radius:12px;font-weight:600;cursor:pointer;box-shadow:0 4px 15px rgba(5,150,105,0.3);text-decoration:none;transition:all 0.3s ease;margin:0 0.5rem;";
                            btn.innerHTML = `
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <polygon points="10 8 16 12 10 16"></polygon>
                                </svg>
                                Voir le site en direct
                            `;
                            
                            btn.addEventListener("click", (e) => {{
                                e.preventDefault();
                                this.open();
                            }});
                            
                            container.prepend(btn);
                        }}
                        
                        createModal() {{
                            const modalHTML = `
                                <div class="hubmairie-modal-overlay" id="hubmairieModal">
                                    <div class="hubmairie-modal">
                                        <div class="hubmairie-modal-header">
                                            <div style="display:flex;align-items:center;gap:0.75rem;font-weight:600;color:white;">
                                                Prévisualisation en direct
                                            </div>
                                            <div style="display:flex;gap:0.5rem;align-items:center;">
                                                <button class="hubmairie-device-btn active" data-device="desktop" title="Bureau" style="width:44px;height:44px;border-radius:10px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:white;cursor:pointer;">💻</button>
                                                <button class="hubmairie-device-btn" data-device="tablet" title="Tablette" style="width:44px;height:44px;border-radius:10px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:white;cursor:pointer;">📱</button>
                                                <button class="hubmairie-device-btn" data-device="phone" title="Mobile" style="width:44px;height:44px;border-radius:10px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:white;cursor:pointer;">📞</button>
                                                <button class="hubmairie-close-btn" title="Fermer" style="width:44px;height:44px;border-radius:10px;background:rgba(220,38,38,0.8);border:none;color:white;cursor:pointer;margin-left:1rem;font-weight:bold;">✕</button>
                                            </div>
                                        </div>
                                        <div class="hubmairie-modal-body" style="flex:1;background:#0F172A;padding:2rem;display:flex;justify-content:center;align-items:center;overflow:auto;">
                                            <div id="previewFrame"></div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            
                            document.body.insertAdjacentHTML("beforeend", modalHTML);
                            this.modal = document.getElementById("hubmairieModal");
                            this.frameContainer = document.getElementById("previewFrame");
                            
                            this.modal.querySelector(".hubmairie-close-btn").addEventListener("click", () => this.close());
                            this.modal.addEventListener("click", (e) => {{
                                if (e.target === this.modal) this.close();
                            }});
                            
                            document.addEventListener("keydown", (e) => {{
                                if (e.key === "Escape" && this.modal.classList.contains("active")) {{
                                    this.close();
                                }}
                            }});
                            
                            this.modal.querySelectorAll(".hubmairie-device-btn").forEach(b => {{
                                b.addEventListener("click", () => this.switch(b.dataset.device));
                            }});
                        }}
                        
                        open() {{
                            this.modal.classList.add("active");
                            document.body.style.overflow = "hidden";
                            this.switch(this.current);
                        }}
                        
                        close() {{
                            this.modal.classList.remove("active");
                            document.body.style.overflow = "";
                            this.frameContainer.innerHTML = "";
                        }}
                        
                        switch(device) {{
                            this.current = device;
                            this.modal.querySelectorAll(".hubmairie-device-btn").forEach(b => {{
                                if (b.dataset.device === device) {{
                                    b.classList.add("active");
                                    b.style.background = "#0066CC";
                                }} else {{
                                    b.classList.remove("active");
                                    b.style.background = "rgba(255,255,255,0.1)";
                                }}
                            }});
                            
                            let html = "";
                            if (device === "phone") {{
                                html = `<div style="width:375px;height:812px;background:#000;border-radius:55px;padding:14px;box-shadow:0 30px 80px rgba(0,0,0,0.8);position:relative;transform:scale(0.8);"><div style="width:100%;height:100%;background:white;border-radius:inherit;overflow:hidden;"><iframe src="${{this.url}}" allowfullscreen style="width:100%;height:100%;border:none;"></iframe></div></div>`;
                            }} else if (device === "tablet") {{
                                html = `<div style="width:820px;height:1100px;background:#000;border-radius:40px;padding:20px;box-shadow:0 35px 90px rgba(0,0,0,0.7);transform:scale(0.6);"><div style="width:100%;height:100%;background:white;border-radius:inherit;overflow:hidden;"><iframe src="${{this.url}}" allowfullscreen style="width:100%;height:100%;border:none;"></iframe></div></div>`;
                            }} else {{
                                html = `<div style="width:100%;max-width:1200px;height:100%;background:#111;border-radius:12px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.6);"><iframe src="${{this.url}}" allowfullscreen style="width:100%;height:100%;border:none;"></iframe></div>`;
                            }}
                            this.frameContainer.innerHTML = html;
                        }}
                    }}
                    
                    new PreviewModal();
                }});
            }})();
        </script>
    """
    
    return mark_safe(js_code)


# =============================================================================
# MENU : RESTREINDRE POUR NON SUPERUSERS
# =============================================================================

@hooks.register("construct_main_menu")
def hide_snippets_menu_for_non_admins(request, menu_items):
    if not request.user.is_superuser:
        allowed = {"explorer", "images", "documents", "reports", "settings"}
        menu_items[:] = [item for item in menu_items if getattr(item, "name", "") in allowed]


# =============================================================================
# SNIPPETS PERSONNALISÉS
# =============================================================================

class MembreEquipeViewSet(SnippetViewSet):
    model = None  # Remplace par ton modèle réel
    icon = "group"
    menu_label = "Équipe municipale"
    menu_order = 300
    add_to_admin_menu = True


class FAQViewSet(SnippetViewSet):
    model = None  # Remplace par ton modèle réel
    icon = "help"
    menu_label = "FAQ"
    menu_order = 400
    add_to_admin_menu = True


class PartenairesViewSet(SnippetViewSet):
    model = None  # Remplace par ton modèle réel
    icon = "group"
    menu_label = "Partenaires"
    menu_order = 500
    add_to_admin_menu = True


# =============================================================================
# DASHBOARD PERSONNALISÉ
# =============================================================================

class HubMairieWelcomePanel:
    order = 10

    def __init__(self, request):
        self.request = request

    @property
    def media(self):
        from django.forms.widgets import Media
        return Media()

    def render(self):
        User = get_user_model()
        stats = {
            "total": Page.objects.count(),
            "live": Page.objects.live().count(),
            "draft": Page.objects.not_live().count(),
            "users": User.objects.count(),
        }
        return format_html(
            """
            <section class="nice-padding" style="background:white;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,0.1);margin-bottom:1.5rem;overflow:hidden;">
                <div style="background:linear-gradient(135deg,#0C1E3C,#163A5F,#0066CC);padding:2rem;color:white;">
                    <h2 style="margin:0;font-size:1.8rem;font-weight:700;display:flex;align-items:center;gap:1rem;">
                        <span style="width:48px;height:48px;background:rgba(255,255,255,0.15);border-radius:12px;display:grid;place-items:center;">
                            Home Icon
                        </span>
                        Bienvenue sur HubMairie
                    </h2>
                    <p style="margin:0.5rem 0 0;font-size:1rem;opacity:0.9;">
                        Gestion complète du site de votre mairie — Sans code
                    </p>
                </div>
                <div style="padding:1.5rem;display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;">
                    <div style="text-align:center;padding:1rem;background:#F0F9FF;border-radius:12px;">
                        <div style="font-size:2.2rem;font-weight:700;color:#0066CC;">{total}</div>
                        <div style="color:#64748B;font-size:0.875rem;">Pages totales</div>
                    </div>
                    <div style="text-align:center;padding:1rem;background:#ECFDF5;border-radius:12px;">
                        <div style="font-size:2.2rem;font-weight:700;color:#059669;">{live}</div>
                        <div style="color:#64748B;font-size:0.875rem;">Publiées</div>
                    </div>
                    <div style="text-align:center;padding:1rem;background:#FFFBEB;border-radius:12px;">
                        <div style="font-size:2.2rem;font-weight:700;color:#D97706;">{draft}</div>
                        <div style="color:#64748B;font-size:0.875rem;">Brouillons</div>
                    </div>
                    <div style="text-align:center;padding:1rem;background:#F5F3FF;border-radius:12px;">
                        <div style="font-size:2.2rem;font-weight:700;color:#7C3AED;">{users}</div>
                        <div style="color:#64748B;font-size:0.875rem;">Utilisateurs</div>
                    </div>
                </div>
            </section>
            """,
            **stats
        )


@hooks.register("construct_homepage_panels")
def add_hubmairie_dashboard(request, panels):
    panels.insert(0, HubMairieWelcomePanel(request))
