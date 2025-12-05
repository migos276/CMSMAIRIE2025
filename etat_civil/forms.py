"""
Formulaires pour les demandes d'actes d'état civil.
"""
from django import forms
from .models import ActeNaissance, ActeMariage, ActeDeces, LivretFamille


class BaseActeForm(forms.ModelForm):
    """Formulaire de base pour les actes."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter les classes Tailwind à tous les champs
        for field_name, field in self.fields.items():
            css_class = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3
            if isinstance(field.widget, forms.DateInput):
                field.widget = forms.DateInput(attrs={'type': 'date', 'class': css_class})
            else:
                field.widget.attrs['class'] = css_class


class ActeNaissanceForm(BaseActeForm):
    """Formulaire de demande d'acte de naissance."""
    
    class Meta:
        model = ActeNaissance
        fields = [
            'type_acte',
            'demandeur_nom', 'demandeur_prenom', 'demandeur_telephone', 'demandeur_email',
            'nom_concerne', 'prenom_concerne', 'date_naissance', 'lieu_naissance',
            'nom_pere', 'prenom_pere', 'nom_mere', 'prenom_mere',
            'numero_acte_original', 'annee_enregistrement',
            'piece_identite',
        ]
        labels = {
            'demandeur_nom': 'Votre nom',
            'demandeur_prenom': 'Votre prénom',
            'demandeur_telephone': 'Votre téléphone',
            'demandeur_email': 'Votre email',
        }


class ActeMariageForm(BaseActeForm):
    """Formulaire de demande d'acte de mariage."""
    
    class Meta:
        model = ActeMariage
        fields = [
            'type_acte',
            'demandeur_nom', 'demandeur_prenom', 'demandeur_telephone', 'demandeur_email',
            'nom_epoux', 'prenom_epoux', 'date_naissance_epoux',
            'nom_epouse', 'prenom_epouse', 'date_naissance_epouse',
            'date_mariage', 'lieu_mariage',
            'numero_acte_original',
        ]


class ActeDecesForm(BaseActeForm):
    """Formulaire de demande d'acte de décès."""
    
    class Meta:
        model = ActeDeces
        fields = [
            'type_acte',
            'demandeur_nom', 'demandeur_prenom', 'demandeur_telephone', 'demandeur_email',
            'nom_defunt', 'prenom_defunt', 'date_naissance_defunt',
            'date_deces', 'lieu_deces',
            'lien_demandeur',
            'numero_acte_original',
        ]


class LivretFamilleForm(BaseActeForm):
    """Formulaire de demande de livret de famille."""
    
    class Meta:
        model = LivretFamille
        fields = [
            'motif',
            'demandeur_nom', 'demandeur_prenom', 'demandeur_telephone', 'demandeur_email',
            'nom_chef', 'prenom_chef', 'date_naissance_chef',
            'nom_conjoint', 'prenom_conjoint', 'date_naissance_conjoint',
            'date_mariage', 'lieu_mariage',
            'nombre_enfants',
        ]
