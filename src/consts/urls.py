REMOTE = "http://secure-scrubland-6759.herokuapp.com"
REMOTE = "http://localhost:3000"
URL_BASE = REMOTE + "/api/v1/" 

NEW_GAME = "games/new_game.json"
JOIN_GAME = "games/join.json"
SHOW_GAME = "games/{0}.json"

NEW_MOVE = "moves/new_move.json"
WAITING_MOVE_VALIDATION = "moves/waiting_validation.json"
VALIDATE_MOVE = "moves/validate.json"
SHOW_MOVE = "moves/{0}.json"

NEW_GAME_OVER_REQUEST = "game_over_requests/new_game_over_request.json"
WAITING_GAME_OVER_VALIDATION = "game_over_requests/waiting_validation.json"
SHOW_GAME_OVER = "game_over_requests/{0}.json"

SUCCESS = 0
SUCCESS_CODES = [0, 14, 16, 19]
