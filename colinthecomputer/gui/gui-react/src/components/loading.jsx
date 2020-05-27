import React, { Component } from "react";

const Loading = () => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <div class="spinner-grow text-warning" role="status">
        <span class="sr-only">Thinking...</span>
      </div>
      <div class="spinner-grow text-warning" role="status">
        <span class="sr-only">Thinking...</span>
      </div>
      <div class="spinner-grow text-warning" role="status">
        <span class="sr-only">Thinking...</span>
      </div>
    </div>
  );
};

export default Loading;
