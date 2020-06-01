import React, { Component } from "react";

const ErrorPage = (props) => {
  return (
    <div>
      <div
        class="row text-center m-5"
        style={{
          display: "flex",
          alignItems: "center",
        }}
      >
        <h1 style={{ color: "#ff33cc" }}>
          Woah there friend, you might need to slow down!
        </h1>
        <h2
          style={{ fontWeight: "bold" }}
        >{`${props.error.status} ${props.error.text}`}</h2>
      </div>
      <img
        class="rounded float-left mx-5 my-2"
        src="/fun/404.gif"
        alt=""
        style={{ height: "200px" }}
      />
    </div>
  );
};

export default ErrorPage;
