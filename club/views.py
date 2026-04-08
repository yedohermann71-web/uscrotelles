from django.shortcuts import render
from .models import Match


def home(request):
    return render(request, 'club/home.html')


def infos(request):
    return render(request, 'club/infos.html')


def matchs(request):
    matchs = Match.objects.all().order_by('-date')
    return render(request, 'club/matchs.html', {'matchs': matchs})


# ⚽🔥 CLASSEMENT AUTOMATIQUE
def classement(request):

    matchs = Match.objects.all()

    tableau = {}

    for m in matchs:

        if m.score_us is None or m.score_adverse is None:
            continue

        equipe_us = "US Crotelles"
        equipe_adv = m.equipe_adverse

        # init équipe US
        if equipe_us not in tableau:
            tableau[equipe_us] = {"pts": 0, "mj": 0, "g": 0, "n": 0, "p": 0, "bp": 0, "bc": 0}

        # init adversaire
        if equipe_adv not in tableau:
            tableau[equipe_adv] = {"pts": 0, "mj": 0, "g": 0, "n": 0, "p": 0, "bp": 0, "bc": 0}

        # matchs joués
        tableau[equipe_us]["mj"] += 1
        tableau[equipe_adv]["mj"] += 1

        # buts
        tableau[equipe_us]["bp"] += m.score_us
        tableau[equipe_us]["bc"] += m.score_adverse

        tableau[equipe_adv]["bp"] += m.score_adverse
        tableau[equipe_adv]["bc"] += m.score_us

        # résultats
        if m.score_us > m.score_adverse:
            tableau[equipe_us]["pts"] += 3
            tableau[equipe_us]["g"] += 1
            tableau[equipe_adv]["p"] += 1

        elif m.score_us < m.score_adverse:
            tableau[equipe_adv]["pts"] += 3
            tableau[equipe_adv]["g"] += 1
            tableau[equipe_us]["p"] += 1

        else:
            tableau[equipe_us]["pts"] += 1
            tableau[equipe_adv]["pts"] += 1
            tableau[equipe_us]["n"] += 1
            tableau[equipe_adv]["n"] += 1

    classement_final = []

    # 🔥 génération du classement + série
    for equipe, stats in tableau.items():

        serie = ""
        compteur = 0

        for m in reversed(list(matchs)):

            if m.score_us is None or m.score_adverse is None:
                continue

            if equipe == "US Crotelles":
                if m.score_us > m.score_adverse:
                    serie += "V"
                elif m.score_us < m.score_adverse:
                    serie += "D"
                else:
                    serie += "N"
            else:
                # adversaires (simple version)
                if m.score_adverse > m.score_us:
                    serie += "V"
                elif m.score_adverse < m.score_us:
                    serie += "D"
                else:
                    serie += "N"

            compteur += 1
            if compteur == 5:
                break

        classement_final.append({
            "equipe": equipe,
            "pts": stats["pts"],
            "mj": stats["mj"],
            "g": stats["g"],
            "n": stats["n"],
            "p": stats["p"],
            "bp": stats["bp"],
            "bc": stats["bc"],
            "diff": stats["bp"] - stats["bc"],
            "serie": serie[::-1]
        })

    classement_final = sorted(
        classement_final,
        key=lambda x: (x["pts"], x["diff"], x["bp"]),
        reverse=True
    )

    return render(request, 'club/classement.html', {
        'classement': classement_final
    })


def contact(request):
    return render(request, 'club/contact.html')