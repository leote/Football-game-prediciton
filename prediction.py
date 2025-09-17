import csv

# Elo rating functions
def expected_result(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

# Function to convert probability to decimal odds
def probability_to_decimal_odds(probability):
    if probability == 0:
        return "Undefined"
    decimal_odds = 1 / probability
    return f"{decimal_odds:.4f}"

# Load data
elo_ratings = {}
matches = []

try:
    with open('results.csv', 'r', encoding='utf-8') as file: # enter path to .csv file
        reader = csv.DictReader(file)
        for row in reader:
            matches.append(row)
            if row['home_team'] not in elo_ratings:
                elo_ratings[row['home_team']] = 1500
            if row['away_team'] not in elo_ratings:
                elo_ratings[row['away_team']] = 1500
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Compute Elo ratings
for match in matches:
    home = match['home_team']
    away = match['away_team']
    home_rating = elo_ratings[home]
    away_rating = elo_ratings[away]
    
    exp_home = expected_result(home_rating, away_rating)
    
    try:
        home_score = int(match['home_score'])
        away_score = int(match['away_score'])
        
        if home_score > away_score:
            actual_home = 1
        elif home_score == away_score:
            actual_home = 0.5
        else:
            actual_home = 0
            
        # Update Elo ratings
        elo_ratings[home] = home_rating + 30 * (actual_home - exp_home)
        elo_ratings[away] = away_rating + 30 * ((1-actual_home) - (1-exp_home))
    except:
        continue

# Prediction
home_team = input("\nEnter home team: ")
away_team = input("Enter away team: ")

if home_team not in elo_ratings or away_team not in elo_ratings:
    print("Team not found in database")
else:
    home_elo = elo_ratings[home_team]
    away_elo = elo_ratings[away_team]
    
    prob_home = expected_result(home_elo, away_elo)
    prob_away = 1 - prob_home
    
    # Calculate decimal odds
    home_odds = probability_to_decimal_odds(prob_home)
    away_odds = probability_to_decimal_odds(prob_away)
    
    print(f"\n--- {home_team} vs {away_team} ---")
    print(f"Elo Ratings: {home_team} ({round(home_elo)}) vs {away_team} ({round(away_elo)})")
    print(f"\nWin Probability:")
    print(f"{home_team}: {prob_home*100:.1f}%")
    print(f"{away_team}: {prob_away*100:.1f}%")
    
    print(f"\nTrue Odds:")
    print(f"{home_team}: {home_odds}")

    print(f"{away_team}: {away_odds}")
