from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Zawody, Sedzia, ZawodyGrupa, ZawodyDynamic, SedziaDynamic, ZawodnicyDruzyny, Druzyna
from account.models import Account
from django.db.models.functions import Concat
from django.db.models import Value, CharField, TextField
from django.db.models import Q
from django.core.exceptions import ValidationError


class ZawodyModelForm(forms.ModelForm):
	class Meta:
		model = Zawody
		fields = (
			'nazwa',
			'zawody_grupa',
			'liczba_strzalow',
			'turniej',
			'oplata_konkurencja',
			'oplata_bron',
			'oplata_amunicja',

			)
	def __init__(self, *args, **kwargs):
		super(ZawodyModelForm, self).__init__(*args, **kwargs)
		self.fields['liczba_strzalow'].label = 'Liczba strzałów'
		self.fields['zawody_grupa'].label = 'Grupa konkurencji'
		self.fields['oplata_konkurencja'].label = 'Opłata za konkurencję'
		self.fields['oplata_bron'].label = 'Opłata za broń'
		self.fields['oplata_amunicja'].label = 'Opłata za amunicję'



class ZawodyDynamicModelForm(forms.ModelForm):
	class Meta:
		model = ZawodyDynamic
		fields = (
			'nazwa',
			'turniej',
			'oplata_konkurencja',
			'oplata_bron',
			'oplata_amunicja',
			'miss',
			'procedura',
			'noshoot'

			)

	def __init__(self, *args, **kwargs):
		super(ZawodyDynamicModelForm, self).__init__(*args, **kwargs)
		self.fields['oplata_konkurencja'].label = 'Opłata za konkurencję'
		self.fields['oplata_bron'].label = 'Opłata za broń'
		self.fields['oplata_amunicja'].label = 'Opłata za amunicję'
		self.fields['miss'].label = 'Wartość referencyjna Miss'
		self.fields['procedura'].label = 'Wartość referencyjna procedura'
		self.fields['noshoot'].label = 'Wartość referencyjna NoShoot'
#formularz przypisywania sędziego do konkurencji

class SedziaModelForm(forms.ModelForm):
	# pk = kwargs.pop('zawody_pk', None)
	# zawody = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset= Zawody.objects.all())
	# sedzia	 = forms.CharField(widget=forms.TextInput())

	class Meta:
		model = Sedzia
		fields = (
			'zawody',
			'sedzia',
			)
	def __init__(self, *args, **kwargs):
		pk = kwargs.pop('zawody_pk', None)
		super(SedziaModelForm, self).__init__(*args, **kwargs)
		# print(f'pk is: {pk}')

		#w propertce sedzia możemy wybrać tylko takiego usera, który jest sędzią lub rtsem
		self.fields['sedzia'].queryset = self.fields['sedzia'].queryset.filter(is_sedzia=1) | self.fields['sedzia'].queryset.filter(rts=1)
		self.fields['zawody'].queryset = self.fields['zawody'].queryset.filter(turniej=pk)
		
		# self.fields['sedzia'].label = 'Sędzia'


class SedziaModelFormNew(forms.Form):

	qs = Account.objects.filter(is_sedzia=1).annotate(full_name=Concat('nazwisko', Value(' '), 'imie', output_field=CharField())).values_list('id', 'full_name').order_by('full_name')



	def __init__(self, *args, **kwargs):
		print('start')
		pk = kwargs.pop('zawody_pk', None)
		super(SedziaModelFormNew, self).__init__(*args, **kwargs)

		zawody_qs = Zawody.objects.filter(turniej__id=pk).values_list('id', 'nazwa')
		# print(zawody_qs)
		
		# self.fields['sedzia']	 = forms.ChoiceField(widget=forms.Select, choices=self.qs)
		self.fields['sedzia']	 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=self.qs)
		self.fields['zawody']	 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=zawody_qs)

		# self.fields['sedzia'].label = 'Sędzia'

class SedziaDynamicModelForm(forms.ModelForm):
	class Meta:
		model = SedziaDynamic
		fields = (
			'zawody',
			'sedzia',
			)
	def __init__(self, *args, **kwargs):
		pk = kwargs.pop('zawody_pk', None)
		super(SedziaDynamicModelForm, self).__init__(*args, **kwargs)

		#w propertce sedzia możemy wybrać tylko takiego usera, który jest sędzią lub rtsem
		self.fields['sedzia'].queryset = self.fields['sedzia'].queryset.filter(is_sedzia=1) | self.fields['sedzia'].queryset.filter(rts=1)
		self.fields['zawody'].queryset = self.fields['zawody'].queryset.filter(turniej=pk)




class SedziaDynamicModelFormNew(forms.Form):

	qs = Account.objects.filter(is_sedzia=1).annotate(full_name=Concat('nazwisko', Value(' '), 'imie', output_field=CharField())).values_list('id', 'full_name').order_by('full_name')
	# sett= Account.objects.all()
	# zawody = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = sett)
	# sedzia	 = forms.ChoiceField(widget=forms.Select, choices=qs)
	# sedzia	 = forms.ModelMultipleChoiceField(widget=forms.Select, queryset=Account.objects.filter(Q(is_sedzia=1) | Q(rts=1)))
	# sedzia	 = forms.ModelChoiceField(queryset=Account.objects.filter(Q(is_sedzia=1) | Q(rts=1)))
	# sedzia	 = forms.ChoiceField(widget=forms.Select, choices=Account.objects.all().values_list('id', Concat('nazwisko', Value(' '), 'imie')))
	# zawody = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Zawody.objects.all())






	def __init__(self, *args, **kwargs):
		print('start')
		pk = kwargs.pop('zawody_pk', None)
		super(SedziaDynamicModelFormNew, self).__init__(*args, **kwargs)

		zawody_qs = ZawodyDynamic.objects.filter(turniej__id=pk).values_list('id', 'nazwa')
		# print(zawody_qs)
		
		# self.fields['sedzia']	 = forms.ChoiceField(widget=forms.Select, choices=self.qs)
		self.fields['sedzia']	 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=self.qs)
		self.fields['zawody']	 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=zawody_qs)
		# self.fields['Zawody']	 = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=zawody_qs)
	

		#w propertce sedzia możemy wybrać tylko takiego usera, który jest sędzią lub rtsem
		# self.fields['sedzia'].queryset = self.fields['sedzia'].queryset.filter(is_sedzia=1) | self.fields['sedzia'].queryset.filter(rts=1)
		# self.fields['zawody'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Zawody.objects.filter(id=pk))
		# self.fields['sedzia'].queryset = Account.objects.all()
		# self.fields['zawody'].queryset = self.fields['zawody'].queryset.filter(turniej=pk)
		# self.fields['zawody'].queryset = Zawody.objects.filter(turniej=pk).values_list('id', flat=True)
		# self.fields['zawody'].choices = Zawody.objects.filter(turniej=pk).values_list('id', flat=True)
		
		# self.fields['sedzia'].label = 'Sędzia'



class ZawodyGrupaModelForm(forms.ModelForm):
	class Meta:
		model = ZawodyGrupa
		fields = (
			'nazwa',
			)


class ZawodnicyDruzynyModelForm(forms.ModelForm):
	class Meta:
		model = ZawodnicyDruzyny
		fields = (
			'druzyna',
			'zawodnik',
			)

	def __init__(self, *args, **kwargs):
		from django.forms.widgets import HiddenInput
		druzyna_slug = kwargs.pop('druzyna_slug', None)
		super(ZawodnicyDruzynyModelForm, self).__init__(*args, **kwargs)
		self.fields['druzyna'].widget = HiddenInput()
		self.fields['zawodnik'].queryset = Account.objects.all().order_by('nazwisko')

	def clean(self, *args, **kwargs):
		
		cleaned_data = super().clean()
		druzyna = cleaned_data.get('druzyna')
		zawodnik = cleaned_data.get('zawodnik')
		# print(f'druzyna: {druzyna}')
		liczba_zawodnikow = ZawodnicyDruzyny.objects.filter(druzyna=druzyna).count()
		if liczba_zawodnikow > 3:
			raise ValidationError('Maksymalna liczba zawodników w drużynie to 4')
			self.fields['druzyna'] =druzyna

		if ZawodnicyDruzyny.objects.filter(druzyna=druzyna, zawodnik=zawodnik).count() > 0:
			raise ValidationError('Wybrany zawodnik jest już zapisany do drużyny')
			self.fields['druzyna'] =druzyna
		# print(f'zawodnik zarejestorwany: {zawodnik_juz_zarejestrowany}')
        #sprawdzam czy zawodnik nie jest już przypisany do danej konkurencji
        # if not cleaned_data.get('zawody'):
        #     raise ValidationError('')
        # wybrane_zawody = cleaned_data.get('zawody').id                                                                                                          
        # wybrany_zawodnik = cleaned_data.get('zawodnik').id                                                                                                       
        # if zawodnik_juz_zarejestrowany:                                                                               
            # raise ValidationError("Jesteś już zarejestrowany na te zawody")
            #formularz jest czyszczony więc ustawiam wartość początkową w polu zawodnik na tego zawodnika, który próbuje się zarejestrować
            # self.fields['zawodnik'] =wybrany_zawodnik
class DruzynaModelForm(forms.ModelForm):	
	class Meta:
		model = Druzyna
		fields = (
			'nazwa',
			'administrator',
			'turniej'
			)

	def __init__(self, *args, **kwargs):
		from django.forms.widgets import HiddenInput
		# druzyna_slug = kwargs.pop('druzyna_slug', None)
		super(DruzynaModelForm, self).__init__(*args, **kwargs)
		self.fields['administrator'].widget = HiddenInput()
		self.fields['turniej'].widget = HiddenInput()