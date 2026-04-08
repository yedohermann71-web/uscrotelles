from django.db import models


class Joueur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero = models.IntegerField()
    poste = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='joueurs/', blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Match(models.Model):
    equipe_adverse = models.CharField(max_length=100)
    date = models.DateTimeField()
    lieu = models.CharField(max_length=100)

    score_us = models.IntegerField(null=True, blank=True)
    score_adverse = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"US Crotelles vs {self.equipe_adverse}"

    # 🔥 AJOUT IMPORTANT POUR LE CLASSEMENT
    def resultat(self):
        if self.score_us is None or self.score_adverse is None:
            return None

        if self.score_us > self.score_adverse:
            return "V"
        elif self.score_us == self.score_adverse:
            return "N"
        else:
            return "D"