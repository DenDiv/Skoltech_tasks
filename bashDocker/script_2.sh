 #!/bin/bash
 print_res=`sed 's/<[^>]*>//g ; /^$/d' $1 | sed 's/[^A-Za-z \n]//g' | tr ' ' '\n' | tr -d '\r' | tr -s '\n' | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -nr | head -15`;
 freq_words=`echo "$print_res" | head -10 | awk '{ print $2 }' | tr '\n' ' '`;
 mkdir $2;
 IFS=' ' read -r -a array <<< "$freq_words";
 for word in "${array[@]}"
	do
		touch  $2/"$word".txt;
	done