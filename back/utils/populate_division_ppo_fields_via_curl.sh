curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"finals_player_selection_type\":\"ppo\",\"finals_num_qualifiers_ppo_a\":\"1\",\"finals_num_qualifiers_ppo_b\":\"2\",\"ppo_a_ifpa_range_end\":\"150\",\"division_id\":\"1\",\"finals_num_qualifiers\":\"2\"}" $POPULATE_URL:8000/elizabeth/division/1
