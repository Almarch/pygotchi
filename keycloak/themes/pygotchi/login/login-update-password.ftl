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
    padding: 35px 50px 15px 50px;
  }
</style>

<body>
  <div class="login-wrapper">
    <img class="frame-img" src="${url.resourcesPath}/frame.png" alt="">
    <div class="login-content">
      <form action="${url.loginAction}" method="post">
        <input type="hidden" name="csrfToken" value="${csrfToken!''}"/>
        <#if isAppInitiatedAction??>
          <input type="hidden" name="cancel-aia" value="true"/>
        </#if>
        <div class="field-group">
          <label for="password-new">New Password:</label>
          <input type="password" id="password-new" name="password-new" autocomplete="new-password">
        </div>
        <div class="field-group">
          <label for="password-confirm">Confirm:</label>
          <input type="password" id="password-confirm" name="password-confirm" autocomplete="new-password">
        </div>
        <#-- <#if messagesPerField?? && messagesPerField.existsError('password', 'password-confirm')>
          <div class="field-group">
            <span class="error-text">${kcSanitize(messagesPerField.getFirstError('password', 'password-confirm'))?no_esc}</span>
          </div>
        </#if> -->
        <div class="btn-row">
          <button class="action-btn" type="submit"></button>
        </div>
      </form>
    </div>
  </div>
</body>
</html>
