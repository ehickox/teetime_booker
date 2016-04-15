# teetime_booker
Script that books my favorite golf tee time
___

This script uses the API of a local golf course that I reverse-engineered. Seeing as how this API is very poorly
implemented and obviously insecure, the name of the course and booking website have been obfuscated.

___

#### This script:
1. Figures out when next Sunday is from today, inclusive.
2. Logs into the tee time booking system
3. Retrieves open tee times in the morning
4. If my favorite tee time of 9:30 AM is available, it books it. 
Otherwise, it books the time closest to 9:30, erring on the side of sleeping in if there is a tie.
5. If there are no available tee times in the hour of 9, it prompts to manually
select a time from a list of all available times on the Sunday in question.

