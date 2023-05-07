from django.db import models

class Match(models.Model):
    week = models.IntegerField()
    round_robin = models.IntegerField()
    match_id = models.CharField(max_length=2)
    game = models.IntegerField()
    result = models.IntegerField()
    team = models.CharField(max_length=50)
    opponent = models.CharField(max_length=50)
    side = models.CharField(max_length=3)
    time = models.TimeField()
    player = models.CharField(max_length=50)
    role = models.CharField(max_length=10)
    champion = models.CharField(max_length=50)
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    kda = models.FloatField()
    cs = models.IntegerField()
    cs_per_min = models.FloatField()
    cs_diff = models.IntegerField()
    dmg = models.IntegerField()
    dmg_percent = models.CharField(max_length=10)
    dmg_per_min = models.FloatField()
    kp_percent = models.CharField(max_length=10)
    gold = models.IntegerField()
    gold_share = models.CharField(max_length=10)
    gold_per_min = models.FloatField()
    dmg_to_gold = models.FloatField()
    
    class Meta:
        db_table = 'match'

    def __str__(self):
        return self.team + " vs " + self.opponent

class Player(models.Model):
    email_address = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    discord_id = models.CharField(max_length=100)
    ign = models.CharField(max_length=100)
    ign2 = models.CharField(max_length=100, blank=True, null=True)
    opgg = models.URLField(max_length=255)
    peak_rank = models.CharField(max_length=100)
    primary_role = models.CharField(max_length=100)

    def __str__(self):
        return self.ign

    class Meta:
        db_table = 'player'

class Team(models.Model):
    team_name = models.CharField(max_length=50)
    group_letter = models.CharField(max_length=1)
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="team1")
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="team2")
    player3 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="team3")
    player4 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="team4")
    player5 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="team5")

    def __str__(self):
        return self.team_name

    class Meta:
        db_table = 'team'