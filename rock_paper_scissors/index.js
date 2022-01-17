const $randomMotion = document.querySelector("#random-motion");
const $matchBtn = document.querySelector("#match-btn");
// const randomNumber = parseInt(Math.random() * 10) % 3;
const rockPaperScissors = ["✌️", "✊", "🖐"];

// $randomMotion.innerHTML = rockPaperScissors[randomNumber];
let randomNumber = 0;
let randomChanger = setInterval(() => {
  randomNumber = parseInt(Math.random() * 10) % 3;
  $randomMotion.innerHTML = rockPaperScissors[randomNumber];
}, 100);

let winCounter = 0;

const matchBtnHandler = (event) => {
  clearInterval(randomChanger);
  const playerResult = event.target.value;
  const result = randomNumber - +playerResult;

  if (result === 0) {
    alert("비겼당");
  } else if (result === -1 || result === 2) {
    document.querySelector("#win-counter").innerHTML = ++winCounter;
    alert("이겼당");
  } else {
    alert("졌당");
  }
  randomChanger = setInterval(() => {
    randomNumber = parseInt(Math.random() * 10) % 3;
    $randomMotion.innerHTML = rockPaperScissors[randomNumber];
  }, 100);
};

$matchBtn.addEventListener("click", (event) => {
  if (event.target.tagName === "BUTTON") {
    matchBtnHandler(event);
  }
});
