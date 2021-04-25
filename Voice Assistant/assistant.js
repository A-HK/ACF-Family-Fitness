//const startBtn = document.createElement("button");
//startBtn.innerHTML = "Start listening";
const startBtn = document.getElementById("start")
const result = document.createElement("div");
const processing = document.createElement("p");
document.body.append(startBtn);
document.body.append(result);
document.body.append(processing);

// speech to text
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let toggleBtn = null;
if (typeof SpeechRecognition === "undefined") {
	startBtn.remove();
	result.innerHTML = "<b>Browser does not support Speech API. Please download latest chrome.<b>";
} else {
	const recognition = new SpeechRecognition();
	recognition.continuous = true;
	recognition.interimResults = true;
	recognition.onresult = event => {
		const last = event.results.length - 1;
		const res = event.results[last];
		const text = res[0].transcript;
		if (res.isFinal) {
			processing.innerHTML = "processing ....";

			const response = process(text);
			const p = document.createElement("p");
			p.innerHTML = `You said: ${text} </br>Siri said: ${response}`;
			processing.innerHTML = "";
			result.appendChild(p);

			// text to speech
			speechSynthesis.speak(new SpeechSynthesisUtterance(response));
		} else {
			processing.innerHTML = `listening: ${text}`;
		}
	}
	let listening = false;
	toggleBtn = () => {
		if (listening) {
			recognition.stop();
			startBtn.textContent = "Start listening";
		} else {
			recognition.start();
			startBtn.textContent = "Stop listening";
		}
		listening = !listening;
	};
	startBtn.addEventListener("click", toggleBtn);

}

// processor
function process(rawText) {
	let text = rawText.replace(/\s/g, "");
	text = text.toLowerCase();
	let response = null;
	switch(text) {
		case "hello":
			response = "hi, how are you doing?"; break;
		case "what'syourname":
			response = "My name's Siri.";  break;
		case "howareyou":
			response = "I'm good."; break;
    case "exerciseforchildren":
      response = "Children and adolescents ages 6 through 17 years should do 60 minutes (1 hour) or more of moderate-to-vigorous intensity physical activity each day, including daily aerobic – and activities that strengthen bones (like running or jumping) – 3 days each week, and that build muscles. "; break;
    case "givemeageneralrecommendation":
  		response = "Get at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous aerobic activity a week, or a combination of moderate and vigorous activity."; break;
		case "whattimeisit":
			response = new Date().toLocaleTimeString(); break;
		case "stop":
			response = "Bye!!";
			toggleBtn();
	}
	if (!response) {
		window.open(`http://google.com/search?q=${rawText.replace("search", "")}`, "_blank");
		return `I found some information for ${rawText}`;
	}
	return response;
}

speechSynthesis.speak(new SpeechSynthesisUtterance(response));
