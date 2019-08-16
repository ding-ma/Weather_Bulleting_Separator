# Weather Bulletin Parser
There is two programs in here:
* Quebec Health Index text parser
* XML exception in smoke parser
Both programs are writting in pure python with the help of xml.tree and regex.

# XML parser
Before having the XML files, I tried parsing text with regex. However, there was little to no order in the text file thus it was really hard to program.
The program takes the xml files in a repository, it search if it contains the tag "airQualityHealthIndexInSmoke". It returns the value as well as the original index.
- Dealing with hours and timezones was the challenging part of this project. I had to take into account if it was standard or daylight time.

# QHI parser
This text parser is more straight forward because of its consistent format. Each region has a regex created and added into a list. Then, the program iterates through the list to find the air index. 
- The hardest part of this project was writing regex that would take into account all edge cases.
