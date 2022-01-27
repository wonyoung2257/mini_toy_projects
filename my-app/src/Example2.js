import { useState } from "react";

const Example2 = () => {
  const [text, setText] = useState("텍스트");

  const changeHandler = (e) => {
    setText(e.target.value);
  };

  return (
    <div>
      <input onChange={changeHandler} />
      <h1>{text}</h1>
    </div>
  );
};

export default Example2;
