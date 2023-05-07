from django.shortcuts import get_object_or_404, render
from collections import defaultdict
from django.db.models import Avg, Count, F, Q, FloatField
from django.core.exceptions import ObjectDoesNotExist
from .models import Match, Player, Team

def match_list(request):
    matches = Match.objects.all()
    return render(request, 'playerdata/match_list.html', {'matches': matches})

def player_list(request):
    players = Player.objects.all()
    return render(request, 'playerdata/player_list.html', {'players': players})

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'playerdata/team_list.html', {'teams': teams})

def home(request):
    roles = ["TOP", "JUNGLE", "MID", "BOT", "SUPPORT"]
    ranks = ["BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTERS", "GRANDMASTER", "CHALLENGER"]

    players = Player.objects.all()

    # Fetch the teams and group them by group letter
    teams = Team.objects.all().order_by('group_letter', 'team_name')
    grouped_teams = defaultdict(list)
    for team in teams:
        grouped_teams[team.group_letter].append(team)

    context = {
        'players': players,
        'roles': roles,
        'ranks': ranks,
        'grouped_teams': grouped_teams,
        'range': range(4),  # Assuming each group has exactly 4 teams
    }

    return render(request, 'playerdata/index.html', context)


def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    
    # Fetch the player's match data from the database
    match_data = Match.objects.filter(player=player)

    # Calculate the overall stats
    num_matches = match_data.count()
    num_wins = match_data.filter(result=True).count()
    total_kda = sum([(m.kills + m.assists) / max(1, m.deaths) for m in match_data])
    total_cs = sum([m.cs for m in match_data])
    total_gold = sum([m.gold for m in match_data])
    total_gold_percentage = sum([m.gold_share for m in match_data])
    total_dmg_percentage = sum([m.dmg_percent for m in match_data])
    total_kp_percentage = sum([m.kp_percent for m in match_data])
    total_cs_diff = sum([m.cs_diff for m in match_data])
    total_dmg_per_gold = sum([m.dmg / m.gold for m in match_data])

    overall_stats = {
        'record': f"{num_wins} - {num_matches - num_wins}",
        'win_rate': f"{num_wins / num_matches * 100:.2f}%",
        'kda': f"{total_kda / num_matches:.2f}",
        'cs_per_min': f"{total_cs / (sum([m.time.total_seconds() for m in match_data]) / 60):.2f}",
        'gold_per_min': f"{total_gold / (sum([m.time.total_seconds() for m in match_data]) / 60):.2f}",
        'gold_percentage': f"{total_gold_percentage / num_matches:.2f}%",
        'dmg_percentage': f"{total_dmg_percentage / num_matches:.2f}%",
        'kp_percentage': f"{total_kp_percentage / num_matches:.2f}%",
        'cs_diff': f"{total_cs_diff / num_matches:.2f}",
        'dmg_per_gold': f"{total_dmg_per_gold / num_matches:.4f}",
    }

    # Calculate champion-specific stats
    champion_stats = {}
    for match in match_data:
        champion = match.champion
        if champion not in champion_stats:
            champion_stats[champion] = {
                'champ_name': champion,
                'games_played': 0,
                'wins': 0,
                'total_kda': 0,
                'total_cs': 0,
                'total_gold': 0,
                'total_time': 0,
                'total_gold_percentage': 0,
                'total_dmg_percentage': 0,
                'total_kp_percentage': 0,
                'total_cs_diff': 0,
                'total_dmg_per_gold': 0,
            }

        champion_stats[champion]['games_played'] += 1
        if match.result:
            champion_stats[champion]['wins'] += 1

        champion_stats[champion]['total_kda'] += (match.kills + match.assists) / max(1, match.deaths)
        champion_stats[champion]['total_cs'] += match.cs
        champion_stats[champion]['total_gold'] += match.gold
        champion_stats[champion]['total_time'] += match.time.total_seconds()
        champion_stats[champion]['total_gold_percentage'] += match.gold_share
        champion_stats[champion]['total_dmg_percentage'] += match.dmg_percent
        champion_stats[champion]['total_kp_percentage'] += match.kp_percent
        champion_stats[champion]['total_cs_diff'] += match.cs_diff
        champion_stats[champion]['total_dmg_per_gold'] += match.dmg / max(1, match.gold)

    # Calculate averages and format the stats for display
    for champ, stats in champion_stats.items():
        games_played = stats['games_played']
        stats.update({
            'record': f"{stats['wins']} - {games_played - stats['wins']}",
            'win_rate': f"{stats['wins'] / games_played * 100:.2f}%",
            'kda': f"{stats['total_kda'] / games_played:.2f}",
            'cs_per_min': f"{stats['total_cs'] / max(1, (stats['total_time'] / 60)):.2f}",
            'gold_per_min': f"{stats['total_gold'] / max(1, (stats['total_time'] / 60)):.2f}",
            'gold_percentage': f"{stats['total_gold_percentage'] / games_played:.2f}%",
            'dmg_percentage': f"{stats['total_dmg_percentage'] / games_played:.2f}%",
            'kp_percentage': f"{stats['total_kp_percentage'] / games_played:.2f}%",
            'cs_diff': f"{stats['total_cs_diff'] / games_played:.2f}",
            'dmg_per_gold': f"{stats['total_dmg_per_gold'] / games_played:.4f}",
        })

    # Sort champion stats by most played
    champion_stats = sorted(champion_stats.values(), key=lambda x: x['games_played'], reverse=True)


    return render(request, 'playerdata/player_detail.html', {'player': player, 'overall_stats': overall_stats, 'champion_stats': champion_stats, 'matches': match_data})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    
    # Get all matches with the team as either team or opponent
    all_matches = Match.objects.filter(Q(team=team.team_name) | Q(opponent=team.team_name)).order_by('id')
    
    # Create separate lists for self and opponent matches
    self_matches = [match for match in all_matches if match.team == team.team_name]
    opp_matches = [match for match in all_matches if match.opponent == team.team_name]

    # Group matches into chunks of 5
    grouped_self_matches = [self_matches[i:i + 5] for i in range(0, len(self_matches), 5)]
    grouped_opp_matches = [opp_matches[i:i + 5] for i in range(0, len(opp_matches), 5)]

    # Combine self and opponent matches into a single list of groups
    grouped_matches = []
    for self_group, opp_group in zip(grouped_self_matches, grouped_opp_matches):
        match_group = {
            'matches': list(zip(self_group, opp_group))
        }
        grouped_matches.append(match_group)

    # Calculate the overall record for the team
    team_matches = Match.objects.filter(Q(team=team.team_name)).order_by('id')
    num_matches = team_matches.count() / 5
    num_wins = team_matches.filter(result=1).count() / 5
    overall_record = f"{num_wins} - {num_matches - num_wins}"

    # Fetch the team's player data from the database
    players = Player.objects.filter(
        Q(team1=team) | Q(team2=team) | Q(team3=team) | Q(team4=team) | Q(team5=team)
    )
    
    player_data = {}
    for player in players:
        match_data = Match.objects.filter(player=player.ign)

        player_data[player] = {
            'avg_dmg': f"{match_data.aggregate(Avg('dmg_percent'))['dmg_percent__avg']:.2f}",
            'avg_gold_share': f"{match_data.aggregate(Avg('gold_share'))['gold_share__avg']:.2f}",
            'champion_stats': {},
        }

        for match in match_data:
            champion = match.champion
            if champion not in player_data[player]['champion_stats']:
                player_data[player]['champion_stats'][champion] = {
                    'champ_name': champion,
                    'games_played': 0,
                    'wins': 0,
                    'total_kda': 0,
                }

            player_data[player]['champion_stats'][champion]['games_played'] += 1
            if match.result == 1:
                player_data[player]['champion_stats'][champion]['wins'] += 1

            player_data[player]['champion_stats'][champion]['total_kda'] += (match.kills + match.assists) / max(1, match.deaths)

        # Calculate averages and format the champion stats for display
        for champ, stats in player_data[player]['champion_stats'].items():
            games_played = stats['games_played']
            stats.update({
                'record': f"{stats['wins']} - {games_played - stats['wins']}",
                'kda': f"{stats['total_kda'] / games_played:.2f}",
            })

        # Sort champion stats by most played
        player_data[player]['champion_stats'] = sorted(player_data[player]['champion_stats'].values(), key=lambda x: x['games_played'], reverse=True)

    return render(request, 'playerdata/team_detail.html', {'team': team, 'grouped_matches': grouped_matches, 'player_data': player_data, 'overall_record' : overall_record})

def champ_stats(request):
    match_data = Match.objects.all()
    champion_stats = {}
    for match in match_data:
        champion = match.champion
        if champion not in champion_stats:
            champion_stats[champion] = {
                'champ_name': champion,
                'games_played': 0,
                'wins': 0,
                'total_kills': 0,
                'total_deaths': 0,
                'total_assists': 0,
                'total_cs': 0,
                'total_gold': 0,
                'total_time': 0,
                'total_gold_percentage': 0,
                'total_dmg_percentage': 0,
                'total_kp_percentage': 0,
                'total_cs_diff': 0,
                'total_dmg_per_gold': 0,
                'total_dmg': 0,
            }

        champion_stats[champion]['games_played'] += 1
        if match.result:
            champion_stats[champion]['wins'] += 1

        champion_stats[champion]['total_kills'] += match.kills
        champion_stats[champion]['total_deaths'] += match.deaths
        champion_stats[champion]['total_assists'] += match.assists
        champion_stats[champion]['total_cs'] += match.cs
        champion_stats[champion]['total_gold'] += match.gold
        champion_stats[champion]['total_time'] += match.time.total_seconds()
        champion_stats[champion]['total_gold_percentage'] += match.gold_share
        champion_stats[champion]['total_dmg_percentage'] += match.dmg_percent
        champion_stats[champion]['total_kp_percentage'] += match.kp_percent
        champion_stats[champion]['total_cs_diff'] += match.cs_diff
        champion_stats[champion]['total_dmg_per_gold'] += match.dmg / match.gold
        champion_stats[champion]['total_dmg'] += match.dmg

    for champ, stats in champion_stats.items():
        games_played = stats['games_played']
        total_time = stats['total_time'] / 60
        stats.update({
            'record': f"{stats['wins']} - {games_played - stats['wins']}",
            'win_rate': f"{stats['wins'] / games_played * 100:.2f}%",
            'avg_kills': stats['total_kills'] / games_played,
            'avg_deaths': stats['total_deaths'] / games_played,
            'avg_assists': stats['total_assists'] / games_played,
            'avg_cs_per_min': stats['total_cs'] / total_time,
            'avg_gold_per_min': stats['total_gold'] / total_time,
            'avg_gold_percentage': stats['total_gold_percentage'] / games_played,
            'avg_dmg_percentage': stats['total_dmg_percentage'] / games_played,
            'avg_kp_percentage': stats['total_kp_percentage'] / games_played,
            'avg_cs_diff': stats['total_cs_diff'] / games_played,
            'avg_dmg_per_gold': stats['total_dmg_per_gold'] / games_played,
            'avg_dmg_per_min': stats['total_dmg'] / total_time,
            'avg_kda': (stats['total_kills'] + stats['total_assists']) / max(stats['total_deaths'], 1),
        })

    champion_stats = sorted(champion_stats.values(), key=lambda x: x['games_played'], reverse=True)

    return render(request, 'playerdata/champ_stats.html', {'champ_stats': champion_stats})


def role_stats(request, role_id):

    if role_id == 1:
        role = 'Top'
    elif role_id == 2:
        role='Jungle'
    elif role_id == 3:
        role='Mid'
    elif role_id == 4:
        role='Bot'
    elif role_id == 5:
        role='Support'

    match_list = Match.objects.filter(role=role)
    player_data = {}

    for match in match_list:
        try:
            player = Player.objects.get(ign=match.player)
        except ObjectDoesNotExist:
            continue
        
        if player not in player_data:
            player_data[player] = {
                'player_name': player.ign,
                'games_played': 0,
                'wins': 0,
                'total_kills': 0,
                'total_deaths': 0,
                'total_assists': 0,
                'total_cs': 0,
                'total_gold': 0,
                'total_time': 0,
                'total_gold_percentage': 0,
                'total_dmg_percentage': 0,
                'total_kp_percentage': 0,
                'total_cs_diff': 0,
                'total_dmg_per_gold': 0,
                'total_dmg': 0,
            }

        player_data[player]['games_played'] += 1
        if match.result:
            player_data[player]['wins'] += 1

        player_data[player]['total_kills'] += match.kills
        player_data[player]['total_deaths'] += match.deaths
        player_data[player]['total_assists'] += match.assists
        player_data[player]['total_cs'] += match.cs
        player_data[player]['total_gold'] += match.gold
        player_data[player]['total_time'] += match.time.total_seconds()
        player_data[player]['total_gold_percentage'] += match.gold_share
        player_data[player]['total_dmg_percentage'] += match.dmg_percent
        player_data[player]['total_kp_percentage'] += match.kp_percent
        player_data[player]['total_cs_diff'] += match.cs_diff
        player_data[player]['total_dmg_per_gold'] += match.dmg / match.gold
        player_data[player]['total_dmg'] += match.dmg

    player_data = {player: stats for player, stats in player_data.items() if stats['games_played'] >= 3}

    for player, stats in player_data.items():
        games_played = stats['games_played']
        total_time = stats['total_time'] / 60
        stats.update({
            'record': f"{stats['wins']} - {games_played - stats['wins']}",
            'win_rate': f"{stats['wins'] / games_played * 100:.2f}%",
            'avg_kills': stats['total_kills'] / games_played,
            'avg_deaths': stats['total_deaths'] / games_played,
            'avg_assists': stats['total_assists'] / games_played,
            'avg_cs_per_min': stats['total_cs'] / total_time,
            'avg_gold_per_min': stats['total_gold'] / total_time,
            'avg_gold_percentage': stats['total_gold_percentage'] / games_played,
            'avg_dmg_percentage': stats['total_dmg_percentage'] / games_played,
            'avg_kp_percentage': stats['total_kp_percentage'] / games_played,
            'avg_cs_diff': stats['total_cs_diff'] / games_played,
            'avg_dmg_per_gold': stats['total_dmg_per_gold'] / games_played,
            'avg_dmg_per_min': stats['total_dmg'] / total_time,
            'avg_kda': (stats['total_kills'] + stats['total_assists']) / max(stats['total_deaths'], 1),

        })

    return render(request, 'playerdata/role_stats.html', {'player_data': player_data, 'role' : role})