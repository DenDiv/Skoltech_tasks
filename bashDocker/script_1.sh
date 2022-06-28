 #!/bin/bash
 print_res=`sed 's/<[^>]*>//g ; /^$/d' $1 | sed 's/[^A-Za-z \n]//g' | tr ' ' '\n' | tr -d '\r' | tr -s '\n' | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -nr | head -10`;
 echo "$print_res";