import en

string ="""
"@yerdua Happy birthday my dear! I hope you are having a wonderful trip."
"@chappellam Thanks for your help yesterday! Let me know how it goes with the Special Effects dye."
"Her yoga mat, much like her soul, was a dark pit of gloom and despair." #yttp http://instagram.com/p/X6EUFnBCCJ/ 
"Yep, pretty much."
 "Eh, it's okay. I saw @amandapalmer perform Purple Rain on NYE; I think I prefer the simarcrulum."
"Prince is playing at DNA Lounge. Um. Wat?"
"Finally making some headway on my project, yayy."
"RT @raganwald: Reminder: "Ignore the haters. You are not the Jackass Whisperer"--@unmarketing"
"RT @pamelafox: I have invented a special expletive for whenever AWS fails us. "Damnazon!"
"@lauraallora Totally! That'd be fun."
"Pulling the Stop Request cord is the best part of riding the bus."
"@djcapelis Yeah! 5 stars. Would recommend. If you like hip-hop."
"Hey there, Ships in the Night. Nice to finally meet you."
"What a glorious time to be alive and queer."
Hard French, here I come.
@daphnekao Thanks!!
@daphnekao Hey! Where did Suzy get her shoes?
Today went by too fast. I want to write more code!
'I' before 'E' except when there's a feisty heist on weird beige foreign neighbours reinventing protein at their leisure.
Oh, Session, you think you're so tough and mysterious, but you're really just a fancy dictionary.
If your day wasn't aesthetically offensive enough, fear not. #The90sCalledAndTheyWantTheirProteinPowderBack pic.twitter.com/TxPS0ZNwkz
@IHazRabies Score! What a come-up.
@Kimberly_Kills do it do it! You'd look hawt with a 'hawk.
@falun Thank you for lunch! It was delicious. I appreciate your insightful perspective.
I'm about to have lunch at Twitter. #meta
@stevieraedrawn congrats! Slash, ugh, that's a long wait.
Paging @queerviolet! You need this in your wardrobe GAYsap. http://bit.ly/ZvkdJV  cc @beastwares
@stevieraedrawn I know you are but what am I? ;-)
@dddagradi @wirehead2501 @numberless Glad I'm not the only one.
I had 3 "a-ha" moments today: lambda functions, enumerate, and exceptions. My brain feels very full.
All my friends who aren't in Hackbright: I miss you! Sorry I've been too overwhelmed to socialize much.
@pamelafox Are. I mean are.
@pamelafox Thanks for coming to talk to us! You ate awesome sauce. <3
@wirehead2501 Aww, thanks! You can't see it in the picture but they have rockets ships on the sides.
@jrronimo Thanks!
dddagradi Ehh, I'm mostly sitting so it's not too bad.
On today's episode of Fashion Forward Or Just Plain Bizarre: I am wearing two different shoes, on...
Walked by a "raw food" food truck. It was just some guy handing people potatoes and shrugging.
@hypatiadotca I just saw that for the first time! It's amazeballs.
Lovers gonna love.
"Every time you see an !, think NOT. It makes the whole internet hilarious." -@lizthedeveloper
@aerialdomo I have! If you ride one and get off at 24th, you exit on the opposite side of the platform. It feels weird.
@KittenKarlyle Srsly! Ugh, sorry you have to deal with that.
Started my period way ahead of schedule. Haaaacccckkkbbbrriiigghhhttt!!! I blame you.
@sukruthasays @falun I'll create it as soon as I have something to ask. When I start my individual project, I'm sure I'll have lots of ?s.
@sukruthasays @falun So... I sat down to do this today, but I don't have any questions for you yet & I felt silly making a blank doc.
@dudeluna The phone was c already disabled by the time I found it. :-( I'm thinking turning it in to the carrier is my best bet.
Trying to reunite a lost iPhone and its owner. All I've got is this photo & a name (Akane). Do you know her? pic.twitter.com/LOeGaV3MyI
@LauraWitwer Thank you so much for your hilarious, heartfelt, and snappily written words. You are my favoritest aerial blogger!
P. S. If you don't oppose sexism in EXACTLY THE RIGHT WAY as judged by your male peers, you'll be subject to rape/death threats. Good luck!
@nelz9999 It was awesome meeting you in person last night! Hope you had fun at the mixer.
@falun It was fabulous to meet you last night! Thanks for fielding my zillions of questions.
@sukruthasays Lovely to meet you last night!! Thanks so much for agreeing to mentor me.
I was thinking the academic-y type fellowship, but that works for the other meanings.
"It's like the database is hard of hearing & will only work if we yell at it: CREATE TABLE!" -@lizthedeveloper on SQL capitalization
Is there a feminist version of the word fellowship? Shellowship?
@StephCircles Aww, I love your answer. Things are topsy turvy here. My life is basically a mash up of xkcd and the L Word.
@StephCircles Heyy Steffi!! How are things in your world?
@stevieraedrawn @queerviolet I agree!

"""
new_string = en.content.categorise(string)
print new_string
for category in new_string:
	print category.name, category.type, category.count