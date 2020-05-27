import React, { Component } from "react";
import Loading from "./loading";

class UserInfo extends Component {
  state = { user_info: null };

  renderGender(gender) {
    switch (gender) {
      case "m":
        return <span class="badge badge-pill badge-info">male</span>;
      case "f":
        return <span class="badge badge-pill badge-info">female</span>;
      case "o":
        return (
          <div style={{ display: "flex", justifyContent: "center" }}>
            <span class="badge badge-pill badge-info">gender: other</span>
          </div>
        );
    }
  }

  renderBirthday(timestamp) {
    var date = new Date(timestamp * 1000);
    var age = new Date(new Date() - date).getFullYear() - 1970;
    return <p>{"born " + date.toDateString() + " (age " + age + " years)"}</p>;
  }

  render() {
    if (!this.state.user_info) {
      return <Loading />;
    }

    var user_info = this.state.user_info;
    return (
      <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <a class="navbar-brand" href="/">
            <img
              src="/icons/colin.PNG"
              width="40px"
              class="d-inline-block align-top"
              alt=""
            />
          </a>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
              <a class="nav-item nav-link" href="/users/">
                <img
                  src="/arrows/back.PNG"
                  width="40px"
                  class="d-inline-block align-top"
                  alt=""
                />
              </a>
            </div>
          </div>
        </nav>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
          }}
        >
          <div
            class="jumbotron"
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              height: "80vh",
            }}
          >
            <div class="col text-center">
              <img src="/icons/user.PNG" alt="" width="100px" />
              <h2>{user_info.username}</h2>
              <h4>{"user #" + user_info.user_id}</h4>
              {this.renderGender(user_info.gender)}
              {this.renderBirthday(user_info.birthday)}
              <a
                href={`/users/${user_info.user_id}/snapshots`}
                role="button"
                class="btn btn-outline-dark"
              >
                view snapshots
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }

  componentDidMount = () => {
    var id = this.props.match.params.user_id;
    fetch(window.api_root + "/users/" + id, {
      method: "GET",
      mode: "cors",
      dataType: "json",
    })
      .then((response) => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response;
      })
      .then((response) => response.json())
      .then((data) => {
        this.setState({ user_info: data });
      })
      .catch((error) => {
        console.log(error); // todo
      });
  };
}

export default UserInfo;
