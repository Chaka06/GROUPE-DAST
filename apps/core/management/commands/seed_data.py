"""
Management command to populate the database with initial demo data.
Run once after the first migrate: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seed the database with initial content for DAST NEWGEN'SPARK"

    def handle(self, *args, **options):
        self._site_settings()
        self._hero_slides()
        self._value_propositions()
        self._services()
        self._portfolio_categories()
        self._blog_categories()
        self._faqs()
        self._admin_user()
        self.stdout.write(self.style.SUCCESS("Données initiales créées avec succès !"))

    def _site_settings(self):
        from apps.core.models import SiteSettings
        obj, created = SiteSettings.objects.get_or_create(pk=1)
        if created or not obj.tagline:
            obj.site_name      = "DAST NEWGEN'SPARK"
            obj.tagline        = "Nous créons des expériences numériques qui transforment"
            obj.tagline_sub    = "Développement web · Marketing digital · Communication · Services numériques"
            obj.about_short    = "Agence numérique spécialisée en développement web, marketing digital, communication et services numériques."
            obj.about_long     = (
                "DAST NEWGEN'SPARK est une agence numérique fondée par des passionnés du digital. "
                "Notre mission est d'accompagner les entreprises, les entrepreneurs et les organisations "
                "dans leur transformation numérique en Côte d'Ivoire et en Afrique. "
                "Nous combinons créativité, technologie et stratégie pour livrer des solutions digitales qui font la différence. "
                "Chaque projet est une opportunité de créer quelque chose d'exceptionnel."
            )
            obj.email_main     = "dastnewgenspark@gmail.com"
            obj.phone_main     = "+225 0173176410"
            obj.whatsapp       = "+2250173176410"
            obj.meta_description = (
                "DAST NEWGEN'SPARK — Agence numérique spécialisée en développement web, "
                "marketing digital, communication et services numériques en Côte d'Ivoire."
            )
            obj.stat_projects  = 50
            obj.stat_clients   = 30
            obj.stat_years     = 3
            obj.stat_team      = 10
            obj.save()
            self.stdout.write("  SiteSettings créé")

    def _hero_slides(self):
        from apps.home.models import HeroSlide
        if HeroSlide.objects.exists():
            return
        HeroSlide.objects.create(
            title="Nous créons des expériences\nnumériques qui transforment",
            subtitle="Développement web · Marketing digital · Communication · Services numériques",
            description="DAST NEWGEN'SPARK accompagne les entreprises dans leur transformation digitale avec des solutions sur mesure, innovantes et performantes.",
            cta_primary_text="Découvrir nos services",
            cta_primary_url="/services/",
            cta_secondary_text="Voir nos réalisations",
            cta_secondary_url="/portfolio/",
            order=1,
            is_active=True,
        )
        self.stdout.write("  HeroSlide créé")

    def _value_propositions(self):
        from apps.home.models import ValueProposition
        if ValueProposition.objects.exists():
            return
        items = [
            ("bx bx-trophy", "Excellence", "Chaque projet est réalisé avec le plus haut niveau d'exigence et de qualité pour dépasser vos attentes.", 1),
            ("bx bx-bulb", "Innovation", "Nous adoptons les technologies les plus récentes pour construire des solutions pérennes et évolutives.", 2),
            ("bx bx-shield-alt-2", "Fiabilité", "Nos engagements sont tenus. Vos projets sont livrés dans les délais et budgets convenus.", 3),
        ]
        for icon, title, desc, order in items:
            ValueProposition.objects.create(icon_class=icon, title=title, description=desc, order=order)
        self.stdout.write("  ValuePropositions créées")

    def _services(self):
        from apps.services.models import Service, ServiceFeature
        if Service.objects.exists():
            return
        services_data = [
            {
                "title": "Développement Web",
                "icon": "bx bx-code-alt",
                "color": "#2B7FD4",
                "short": "Sites web, applications et solutions e-commerce sur mesure, performants et sécurisés.",
                "description": "Nous concevons et développons des sites web et applications web modernes adaptés à vos besoins. Du site vitrine à la plateforme e-commerce complexe, notre équipe maîtrise les technologies front-end et back-end les plus avancées pour vous livrer des solutions robustes, rapides et évolutives.",
                "features": [
                    ("bx bx-check", "Sites vitrines & institutionnels", "Des sites élégants qui reflètent votre image de marque."),
                    ("bx bx-check", "Applications web sur mesure", "Des solutions métier adaptées à vos processus."),
                    ("bx bx-check", "E-commerce & boutiques en ligne", "Des plateformes de vente performantes et sécurisées."),
                    ("bx bx-check", "Optimisation SEO & Performance", "Des sites rapides et bien référencés sur Google."),
                ],
                "order": 1,
            },
            {
                "title": "Marketing Digital",
                "icon": "bx bx-trending-up",
                "color": "#10B981",
                "short": "Stratégie digitale, SEO, publicité en ligne et gestion des réseaux sociaux.",
                "description": "Notre équipe marketing élabore des stratégies digitales complètes pour accroître votre visibilité en ligne et générer des leads qualifiés. Du référencement naturel à la publicité payante, en passant par la gestion des réseaux sociaux, nous vous accompagnons dans toutes vos démarches marketing.",
                "features": [
                    ("bx bx-check", "Référencement naturel (SEO)", "Améliorez votre positionnement sur les moteurs de recherche."),
                    ("bx bx-check", "Publicité en ligne (SEA/SMA)", "Campagnes Google Ads, Facebook Ads, Instagram Ads ciblées."),
                    ("bx bx-check", "Gestion des réseaux sociaux", "Community management et création de contenu engageant."),
                    ("bx bx-check", "Email marketing", "Campagnes d'emailing efficaces pour fidéliser vos clients."),
                ],
                "order": 2,
            },
            {
                "title": "Communication",
                "icon": "bx bxs-megaphone",
                "color": "#F59E0B",
                "short": "Identité visuelle, création de contenu et stratégie de communication globale.",
                "description": "Une communication efficace passe par une identité visuelle forte et des messages clairs. Notre équipe créative vous aide à définir et déployer votre stratégie de communication, de la création de votre charte graphique à la production de vos supports de communication.",
                "features": [
                    ("bx bx-check", "Identité visuelle & Branding", "Logo, charte graphique et guide de style professionnel."),
                    ("bx bx-check", "Création de contenu", "Textes, visuels et vidéos pour tous vos canaux."),
                    ("bx bx-check", "Supports de communication", "Flyers, brochures, kakémonos et supports print."),
                    ("bx bx-check", "Stratégie de communication", "Plan de communication adapté à vos objectifs."),
                ],
                "order": 3,
            },
            {
                "title": "Services Numériques",
                "icon": "bx bx-devices",
                "color": "#8B5CF6",
                "short": "Conseil, formation et accompagnement dans votre transformation numérique.",
                "description": "La transformation numérique est un enjeu majeur pour toutes les organisations. Nous vous accompagnons dans cette transition avec des services adaptés : audit numérique, conseil en digitalisation, formation de vos équipes et mise en place d'outils adaptés à vos besoins.",
                "features": [
                    ("bx bx-check", "Audit numérique", "Évaluation de votre présence digitale et recommandations."),
                    ("bx bx-check", "Conseil en transformation digitale", "Accompagnement stratégique pour votre transition numérique."),
                    ("bx bx-check", "Formation & coaching", "Montée en compétence de vos équipes sur les outils digitaux."),
                    ("bx bx-check", "Solutions logicielles", "Mise en place d'outils de gestion et de productivité."),
                ],
                "order": 4,
            },
        ]
        for data in services_data:
            svc = Service.objects.create(
                title=data["title"],
                slug=slugify(data["title"]),
                icon_class=data["icon"],
                color_accent=data["color"],
                short_description=data["short"],
                description=data["description"],
                featured=True,
                order=data["order"],
            )
            for i, (icon, title, desc) in enumerate(data["features"]):
                ServiceFeature.objects.create(service=svc, icon_class=icon, title=title, description=desc, order=i)
        self.stdout.write("  Services créés")

    def _portfolio_categories(self):
        from apps.portfolio.models import ProjectCategory
        if ProjectCategory.objects.exists():
            return
        for name in ["Développement Web", "Marketing Digital", "Design & Branding", "Applications Mobile"]:
            ProjectCategory.objects.create(name=name, slug=slugify(name))
        self.stdout.write("  Catégories portfolio créées")

    def _blog_categories(self):
        from apps.blog.models import Category
        if Category.objects.exists():
            return
        categories = [
            ("Développement Web", 1),
            ("Marketing Digital", 2),
            ("Design & UX", 3),
            ("Actualités DAST", 4),
            ("Conseils & Astuces", 5),
        ]
        for name, order in categories:
            Category.objects.create(name=name, slug=slugify(name), order=order)
        self.stdout.write("  Catégories blog créées")

    def _faqs(self):
        from apps.core.models import FAQ
        if FAQ.objects.exists():
            return
        faqs = [
            ("Quels types de sites web développez-vous ?", "Nous développons tous types de sites web : sites vitrines, sites institutionnels, e-commerce, blogs, plateformes SaaS et applications web sur mesure. Chaque projet est unique et nous adaptons notre approche à vos besoins spécifiques.", 1),
            ("Quels sont vos délais de livraison ?", "Les délais varient selon la complexité du projet. Un site vitrine simple peut être livré en 2 à 3 semaines. Un projet plus complexe comme une plateforme e-commerce peut nécessiter 6 à 12 semaines. Nous vous communiquons un calendrier précis dès le début du projet.", 2),
            ("Proposez-vous un service de maintenance ?", "Oui, nous proposons des contrats de maintenance qui incluent les mises à jour de sécurité, les sauvegardes régulières, la surveillance de la disponibilité et le support technique. Ces contrats garantissent la pérennité de votre investissement numérique.", 3),
            ("Comment se déroule un projet avec DAST ?", "Notre processus se déroule en 4 étapes : 1) Découverte et analyse de vos besoins, 2) Conception et validation des maquettes, 3) Développement et tests, 4) Lancement et formation. Vous êtes impliqué à chaque étape pour garantir un résultat qui vous correspond.", 4),
            ("Intervenez-vous sur toute la Côte d'Ivoire ?", "Oui, nous travaillons avec des clients sur tout le territoire ivoirien et également à l'international. Grâce aux outils de collaboration en ligne, la distance n'est pas un obstacle à la qualité de nos services.", 5),
            ("Quels sont vos tarifs ?", "Nos tarifs sont adaptés à chaque projet et à chaque budget. Nous proposons des solutions pour les startups, les PME et les grandes entreprises. Contactez-nous pour un devis gratuit et personnalisé.", 6),
        ]
        for question, answer, order in faqs:
            FAQ.objects.create(question=question, answer=answer, order=order)
        self.stdout.write("  FAQs créées")

    def _admin_user(self):
        import os
        from apps.accounts.models import User
        if User.objects.filter(is_owner=True).exists():
            self.stdout.write("  Compte propriétaire déjà existant")
            return
        username  = os.environ.get("SUPER_ADMIN_USERNAME", "dast_owner")
        email     = os.environ.get("SUPER_ADMIN_EMAIL", "dastnewgenspark@gmail.com")
        password  = os.environ.get("SUPER_ADMIN_PASSWORD", "DastAdmin2024!")
        first_name = os.environ.get("SUPER_ADMIN_FIRST_NAME", "SABY")
        last_name  = os.environ.get("SUPER_ADMIN_LAST_NAME", "Ange Noël")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_owner=True,
            role_title="Responsable & Propriétaire",
        )
        self.stdout.write(f"  Compte propriétaire créé : {username} / {password}")
