Kunal Ahuja: You remember I told you the first old block is API is right that is used very limited services now right there are fees. I wanted. There are none but there are a few services, then majorly VM CS move to the new file based. That was the format. I, I, who I extended the last time. Right.

Kunal Ahuja: Yes, and all the validation that extend you along with it goes to SAP right

Kunal Ahuja: Now there are a few services which come through comes to idea to CSP so DMC for us. It just doesn't come through CSP.

Kunal Ahuja: Ok ok it interacts with it only for us it is ok but there are few services. Let's say you have your VR Li log insight cost inside and right

Kunal Ahuja: The way they come, is they are for for for them the services CSP in for CSP is the services ID. So basically they invoke CSP CSP guess of the file.

Kunal Ahuja: We process it we inform CSP the list process and then CSP is responsible for sending to the customer orders obviously right there is no direct interaction between our service and

Kunal Ahuja: Service and

Pallavi Vanaja: ID, I think.

Kunal Ahuja: Early and theoretically but when issues come, they can involve involvement, all the people that who they are pending.

Kunal Ahuja: So now what change. It is. I'll tell you when CSP game, right. First thing that changed was it's been told that they have their own different JSON payload format right like EMC had the whole huge bunch of fields like that with CSP also add their own okay

Kunal Ahuja: Just have

Kunal Ahuja: To be done.

Kunal Ahuja: You can go to this page also what I level and then this validation

Pallavi Vanaja: Yes, I think you already shared that one.

Kunal Ahuja: Don't go with this one. This one is a nod to complete

Kunal Ahuja: The CSP on

Kunal Ahuja: This is the same page where the duplicate calculation I do will do. Right, so feel those limitations.

Okay.

Kunal Ahuja: Okay, so when when CSP came to us. They told me that they're going to come with their own JSON payload format that is when I talk about JSON payload.

Kunal Ahuja: The, the content of the file right that JSON that you had enough. I will be a little different from what we MC is sending but the fields inside that will be almost similar

Pallavi Vanaja: Right. OK.

Kunal Ahuja: So now this is the payload that CSP is giving us right so now let's try to derive who what and when from these right so basically you're who will be subscription ID. Right. Your water will be attributes here data center and ID that is under charge right

Kunal Ahuja: You are WHEN WILL BE FOR JUST USE IT start time, you have the user to record the masses. Right. So these are your who wouldn't so it does the parsing logic is change the restaurant still remains the same. So service submits a file to CSP CSP gets done file to us.

Kunal Ahuja: Okay, right now. One thing to note in this format is if you take this subscription ID VM see us to already give the it said that is starting with them.

Kunal Ahuja: Just what CSP dollars with this format. I'm not going to give you that it food.

Pallavi Vanaja: Okay.

Kunal Ahuja: Who did it on your own. So when the file comes, what we do is

Kunal Ahuja: Before, and only we have that mapping of CSP do it right, said

Pallavi Vanaja: Yes.

Kunal Ahuja: We make sure that corresponding CSP and I dissenters updated in our database table.

Kunal Ahuja: Wherein we maintain these tables, right. So for us in Malaysia. We cash. Some subscription data. We also cash. Some offer data right in that subscription data we have. What is the same, whether that's it is active. What, what is the billing engine that's it belongs to

Kunal Ahuja: What is the corresponding CSP subscription. It does it say and what is the subscription starting right

Kunal Ahuja: Okay. Oh you do validation for that subscription. Last Name Explain right so we load it in memory. And then we do all the validation yeah okay so

Pallavi Vanaja: Then I'll be loading this subscription data from

Kunal Ahuja: We get from SMB border to solo

Kunal Ahuja: Few jobs. First is the have few jobs, one time jobs to get all the SDP fits then incrementally we listened to SMB Q, if there are any status changes or nuisance. We it automatically comes to our database table.

Kunal Ahuja: Okay, same. There's an awful job. We hit offered API every day because all of us are not created very frequently every day our database table gets updated.

Pallavi Vanaja: OK.

Kunal Ahuja: And then, then, then the the workflow as late as yet it loads in in memory, and it does all

Pallavi Vanaja: Does all the revelations allegations. Okay.

Kunal Ahuja: In this case, the flow is user record comes in with CSP subscription ideas. You can see the highlighted one

Kunal Ahuja: I'll check in my

Kunal Ahuja: Basically checking the database table if corresponding it said is there, if not on the fly from that piece of code. Look, I'll make a life cool to CSP to give me the corresponding it said for this because CSP is owner for this life.

Yeah.

Kunal Ahuja: I will get it said, I'll make sure it's updated in my database and then the regulations will go to guide. If it goes back office just understands it said that call is on the fly. If there is a cache miss, basically.

Kunal Ahuja: Okay.

Pallavi Vanaja: Okay, okay. So okay, so this is the

Pallavi Vanaja: Okay, got it. Okay, so both CSP and the job or the service that is actually checking this both will actually essentially get the data from the SMB

Pallavi Vanaja: Or a single database, but just that this particular service looks at the cash and if it doesn't have it in the cash, then it fetches it from CSP.

Kunal Ahuja: Yes, so even SMB, in some cases, might not have this CSP subscription ID and which cases are those. I'll tell you.

Kunal Ahuja: Again when Midas come game right

Kunal Ahuja: When Midas code was put in, then we decided, Dennis and we decided, basically, that they will also store CSP subscription ID.

Kunal Ahuja: So generally, when a new user is created. We didn't really get this to. We don't have to call

Kunal Ahuja: All the mind migrated sets which are coming from SDP even SMB does not have this data.

Kunal Ahuja: So now what happens if the user record comes in for that sense. So, for sure, we will not have the mapping. So that's why we call the API on the fly, and we have dead dad said, if it's a snot drill into number in on the data, the students

Pallavi Vanaja: Okay, so you said a play that's the CSP that is slide.

Pallavi Vanaja: Okay. And where does CSP fetch the

Pallavi Vanaja: It doesn't fetch from Ed w or some particular

Kunal Ahuja: Testing CSP is the owner of this construct basically the USD subscription ID CSP field. It's nowhere. No other services to do anything with it.

Kunal Ahuja: Okay, I mean both of us. It is mentoring other kind of said and CSP maintenance other kind of Sir

Pallavi Vanaja: Yes, yes I I remember you telling you you IDs ESP specific so

Kunal Ahuja: That is when you you add a sense right

Pallavi Vanaja: So wouldn't CSP have its own data store or something where

Kunal Ahuja: They go out there and we query.

Kunal Ahuja: And they have exposed and API to query is basically the query that API. And it gives a corresponding it said

Pallavi Vanaja: Okay. Okay, got it. Okay. Okay.

Kunal Ahuja: With me, we are querying CSP on the fly. If we don't have this information already

Pallavi Vanaja: Okay, okay.

Kunal Ahuja: And once we have it we store it in our data table. So, any, any subsequent record with the same opportunity. We won't call the API again because this team, we have

Pallavi Vanaja: Okay, make sense. Yeah, yeah.

Kunal Ahuja: So that gadget I was talking about is nothing but I agree in America that is based on our database tables into us usage mediation meetings.

Kunal Ahuja: How those data tables are processed.

Kunal Ahuja: We have a few of scheduled jobs which we have from SMB and from offering that we keep on updating

Pallavi Vanaja: Gotcha. Okay. Okay. Yeah.

Kunal Ahuja: Now, though the major problem is solved. We have, we know that it said we know who what and when

Kunal Ahuja: The same set of validation will go through for each and every record.

Pallavi Vanaja: Okay.

Kunal Ahuja: No change, no change at all.

Kunal Ahuja: Only changes coming in interaction with we Mc, Mc SP first changes this which are told to the sub search and it will be CSP zero ID. The second changes.

Kunal Ahuja: When we interact with VM see me directly interact with VM CS SQL, you remember we send notification to their

Pallavi Vanaja: Yes.

Kunal Ahuja: Yes. And there. So you can see anything. Basically what CSP saying is, whenever you want to inform me or do you want to get data from me. They have CSP has build their own framework. I don't know if you're a well known as post office or CSP is notification service.

Pallavi Vanaja: Not yeah okay

Kunal Ahuja: So I believe what it does. You know how Rabbit MQ or any of the messaging us

Pallavi Vanaja: Yeah yeah so

Kunal Ahuja: What they have is they have built a rapper or Amazon is covers like basically you do a run book step of configuring

Kunal Ahuja: Configuring those that is basically they are providing some set of API's in which what you will do is

Kunal Ahuja: You will tell them that I want to create this message type okay message Dave is nothing but a unique, you can

Kunal Ahuja: Compare it to a queue. Right. You want someone to subscribe to that you so that he can get your messages right he or she can get it. So they have kind of created a field, known as message right so if you are a publisher, you will ask them to create a message type. Okay.

Kunal Ahuja: Then you will ask subscriber to subscribe to that message.

Kunal Ahuja: In between what's it is post office who does this job.

Kunal Ahuja: Number I publish

Kunal Ahuja: That message to that any message to that message type whoever a subscriber is on the other end will get that

Pallavi Vanaja: Message. Okay.

Kunal Ahuja: The only thing is, how do you publish it. You don't publish it to you, you hit an API call internally, they maintain their cues and the same way.

Kunal Ahuja: The subscriber has registered that whenever there's a message type or whenever there's a message for this particular message type which the subscriber subscriber, they do a one time activity of telling them, which API to call on this of service layer.

Kunal Ahuja: Basically a CSP or the post office will inform them is through an API.

Pallavi Vanaja: Yeah.

Kunal Ahuja: It's kind of a book.

Pallavi Vanaja: Yeah, and sort of listeners on Bolton, there's like direct calcium

Kunal Ahuja: Their API is on board and in between post office, you're using his notes. Yeah.

Pallavi Vanaja: Okay, okay.

Kunal Ahuja: So that's the only way we interact. There's no other change. So I guess post office. You might know that should be okay for you. It's just think of it as a you know interface between CSP an ID or any other service that CSP is to post office. Yes.

Pallavi Vanaja: Okay, okay.

Kunal Ahuja: So that's. Those are the only two major differences between CSP is no an EMC slow

Kunal Ahuja: When a new service on boards, the management direction is ask them to onboard through CSP, but we are well open, they can follow any moment we support both BMS even CSP because there are few services which comes through which our onboarding and DMC old format. Also, right.

Kunal Ahuja: So, doesn't matter for us, you give any of these two pillows will be able to provide you the processing the usage mediation.

Pallavi Vanaja: Okay, okay.

Kunal Ahuja: All right, now these are the only two methods supported. I mean payloads and I don't think in near future, any third one is going to come

Pallavi Vanaja: Okay.

Kunal Ahuja: Okay, so this is how, if you see this is CSP is paid, basically. So this is how the payload look like right when I've completed the processing, you remember we had sq SP note.

Pallavi Vanaja: When I since

Kunal Ahuja: THE 70s money I have this post office payload in which I have used it, report it. That is a unique ID.

Kunal Ahuja: Service definition ideas will is not relevant to us. Then you have the missing record counts. That means if the customer services provided a total count wrong and we find it to something and current to be live data.

Kunal Ahuja: And then you have failed records the boat, it counts all of the same should have and what is the current interest rate. And if there are any errors, same format, just the fields are different.

Pallavi Vanaja: Got it. Yeah.

Kunal Ahuja: And if you look at this page right this is how you're nervous payload looks like. So inside this message field is the actual content. I want to relate to service.

Kunal Ahuja: Above three fields or post of this specific. So this doesn't care. It's just a configuration so that we need to specify

Pallavi Vanaja: Got it here.

Kunal Ahuja: For it. So if you see this message type

Kunal Ahuja: This is the one that Subscribe. Subscribe. Subscribe services.

Pallavi Vanaja: Okay.

Kunal Ahuja: Now I'll quickly give us a glimpse of your database table. So you have you can just picture Isaac right

Forget

Kunal Ahuja: For

This

Welcome

Kunal Ahuja: So we use SAP HANA for us right

Kunal Ahuja: You see this right we have basically four or five tables. One is your file Metallica, this is nothing but to store every information about the file. What has happened to that file. What is the status, where it's like if you see this tracker ID.

Kunal Ahuja: This is nothing but a unique ID that CSP or EMC gets

Kunal Ahuja: The ID.

I totally

Kunal Ahuja: Fine.

Kunal Ahuja: And this table is don't not separate for EMC CSV. This is for anything come into the UN.

Pallavi Vanaja: Yep. Okay, so that the fields have been mapped to the associated fields.

Kunal Ahuja: Right, good.

Kunal Ahuja: Okay, file process where it is nothing but it unique generation. This is what services, giving me right

Kunal Ahuja: But yes, it is.

Kunal Ahuja: Okay, file, but is where the source file POTUS take some as well. Sell veterinary product family which product family that belongs to

Kunal Ahuja: Status. Where are the status on your local file where I played violin local the local area file path and this is you're basically break down on the total recordable there. How many validation duplicate said of Stevie sap. Wait.

Kunal Ahuja: There's a complete it though. So if you want to start when you're going to kind of dashboard to take this data and see what are happening right

Okay.

Kunal Ahuja: Now this attribute to is basically that means successfully a message was published to post office that's only going to get populated. If it's not that mean it's not going

Pallavi Vanaja: OK.

Kunal Ahuja: I guess the rest of the fields are, you know, pretty much self explanatory. Now, one thing is

Kunal Ahuja: Yes. So, so this is what though there's what the final table is the next table is basically your offer. I'd only right

Kunal Ahuja: So in this VM all the office respective programs and if for example you EMC AWS, you have often have this child. I did his region to see this is basically one

Kunal Ahuja: So this is what we compare and we do offer the relations against, and how does this table gets updated for baby john we hit our API we get any new office and we loaded here.

Kunal Ahuja: Okay. Okay, so that the time of usage validation don't have to hit a PM and Monday night.

Kunal Ahuja: Just to avoid the

Kunal Ahuja: Same way, we have said dash. Right. So if you see the set is there. What is the status.

Kunal Ahuja: What is the product family. What does this start and end date on that said or did and it takes all the validation and also if you see

Kunal Ahuja: So this attribute for is nothing but a CSP view you already. So this is a test system. So that's why you're seeing like this.

Pallavi Vanaja: Okay.

Kunal Ahuja: If you see this right. So this is what I will check when I get the CSP record. I'm going to check whether against us a tribute, for I have a line item in this table or not.

Kunal Ahuja: Gotcha. Not I'm gonna call it a PM. Want to make sure this table is also updated so that I don't have to call up an extreme

Again,

Kunal Ahuja: Just a second.

Kunal Ahuja: So now this is what has happened. So I told you about file table. I told about offer table at all about table duplicate check is basically in memory, some concept of that tune. When we kind of cash. The already present record IDs.

Kunal Ahuja: And this one table is just for operation purpose. Basically, whenever you want to load new families with art, you shouldn't be worried about

Pallavi Vanaja: Okay.

Kunal Ahuja: This is also operation purpose which cash needs to be different. Okay. They don't tell you that we do forking of billing engine where to send the user to SDP or SAP that I cover that.

Kunal Ahuja: Was

Kunal Ahuja: Basically, what happened is

Kunal Ahuja: What happens is now when

Kunal Ahuja: When Midas click then write us a little story. Okay, we are we are ready to switch to file. This we have no problem. But the overall overall decision of switching them to SAP was not get finalized.

Pallavi Vanaja: Okay.

Kunal Ahuja: But that means their subscriptions and still stay in SGP, but they are ready to switch to file this or let's go one step back and just take the MCS example.

Kunal Ahuja: Okay, the way we decided to go perform migration is not a big bang migration, right, because it can impact many customers. What we decided is at the time fee or will be migrated. Okay.

Kunal Ahuja: We're sad right but few ox will still remain in STP.

Kunal Ahuja: Current situation all of the DMC have been migrated. But that's how we started. So during that time.

Kunal Ahuja: This brings us to the situation, wherein since now we MC is going to switch to file based right and that file can have records from a number of folks or all dogs.

Kunal Ahuja: Now out of those fields might have been migrated to SAP fields still be there in SDB made by all know you can play two sets because then finally fit information.

Kunal Ahuja: Yes. Now, when the user record comes in in the file and in the same file, you have a record from SDP and sap both. How do you determine where to send users.

Pallavi Vanaja: Okay.

Kunal Ahuja: Got it.

Pallavi Vanaja: Yeah.

Kunal Ahuja: So the baby data mind that is through this table. Okay, so when SAP when when I when I get this paper when I get the data from SMB, I also get viral that said active

Kunal Ahuja: Even build a building in an SMP or is it active in building has DP.

Pallavi Vanaja: OK. OK.

Kunal Ahuja: OK, so

Kunal Ahuja: Oh,

Kunal Ahuja: Yeah, so it will either it will go to SDP or it will come to SAP. Right. So the way we do. Is this table that I showed you

Kunal Ahuja: Like

Kunal Ahuja: The smell have if you see billing engine, right.

Kunal Ahuja: Mm hmm. How does SMB SMB know that the SMB know this attribute Mike ma whenever we migrate. We make sure the city is migrate status of Satan as DBS migrated. Right. And those updates to keep on getting so we know which billing and then we need Susan

Pallavi Vanaja: OK. OK.

Kunal Ahuja: At a time, it will always be inactive or migrated state if the site is active in both right, by any chance, there's some issue or there's some delay, then we will, by default, assume that it needs to go to SDP

Pallavi Vanaja: Okay.

Kunal Ahuja: What so what what you need to worry about this. There are some forking logic which enables us to send users to SGP and sap both

Kunal Ahuja: On the fly.

Kunal Ahuja: So now to SAP Reagan directly in this through whatever normal who is dB. What we do is, you remember good API flow.

Kunal Ahuja: The order flow. The first diagram that I showed you

Pallavi Vanaja: Yes. Yes. Yeah.

Kunal Ahuja: What we do is we consumed. We put a message in the same view and then the same process goes, it goes into Mongo then Informatica jobs kicks in and Simon's toy.

Pallavi Vanaja: Yes, the same

Pallavi Vanaja: Happens. Okay. Okay.

Kunal Ahuja: You know, they use it should be saying do

Kunal Ahuja: Okay, now, or two. So now everything is done right CSV files are able to consume the MC wells are able to consume all the validation. We have done right now. Other. Now it's time to submit data to SAP right

Kunal Ahuja: So the more you will have SAP we interact to

Kunal Ahuja: Is known as a BCC basically convergent charging what is responsible to perform rating or

Kunal Ahuja: Lead that building amount that I

Pallavi Vanaja: Told you. Right. Yes.

Kunal Ahuja: So we interact with this CC, the way we interact is the tool that we're using this digital route has a native connector to CC, so we don't have to write any specific code to connect to CC

Kunal Ahuja: Okay then.

Kunal Ahuja: We put a hostname and number and credentials. That said, the only thing that we need to do is whatever the sap fields is we need to map our data to those corresponding fields, right, for example, who what and when. What does it say be will map that and some directors to so

Pallavi Vanaja: Okay.

Kunal Ahuja: Now wanted goes to SAP

Kunal Ahuja: Hey, let me cover this next meeting. Actually, I have another one in next year. So I might not be able to cover this for

Pallavi Vanaja: Sure. No, no, no worries. At all. Yeah, definitely.

Kunal Ahuja: So Schedule one for Tuesday.

Kunal Ahuja: And then

Pallavi Vanaja: Show. Yeah. Yeah. No worries. Yeah. Thank you.

Pallavi Vanaja: Bye.

