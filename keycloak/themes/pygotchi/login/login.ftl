<#import "template.ftl" as layout>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaMaGoTcHi</title>
  <link rel="stylesheet" href="${url.resourcesPath}/styles.css">
  <link rel="icon" type="image/png" href="${url.resourcesPath}/favicon.png">
</head>
<style>
  form {
    display: flex;
    flex-direction: column;
    gap: 20px;
    flex: 1;
    justify-content: center;
    padding: 30px 50px 20px 50px;
  }
</style>

<body>
  <div class="login-wrapper">
    <img class="frame-img" src="${url.resourcesPath}/frame.png" alt="">
    <div class="login-content">
      <form action="${url.loginAction}" method="post">
        <input type="hidden" name="csrfToken" value="${csrfToken!''}"/>
        <div class="field-group">
          <label for="username">Player:</label>
          <input type="text" id="username" name="username" autocomplete="username" value="${(login.username)!''}">
        </div>
        <div class="field-group">
          <label for="password">Password:</label>
          <input type="password" id="password" name="password" autocomplete="current-password">
        </div>
        <div class="btn-row">
          <button class="action-btn" type="submit"></button>
        </div>
      </form>
    </div>
  </div>

</body>
</html>
