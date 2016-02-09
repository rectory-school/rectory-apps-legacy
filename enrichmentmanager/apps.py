from django.apps import AppConfig

class EnrichmentManagerConfig(AppConfig):
    name = 'enrichmentmanager'
    verbose_name = "Enrichment Manager"
    
    def ready(self):
        import enrichmentmanager.signals