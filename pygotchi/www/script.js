// Toggle Sidebar Menu
function toggleMenu() {
    const sidebar = document.getElementById("sidebar");
    const menuIcon = document.querySelector(".menu-icon");

    sidebar.classList.toggle("open"); // Toggle sidebar visibility
    menuIcon.classList.toggle("hidden"); // Hide/Show menu icon
}
// Shake Animation on Image Click
document.getElementById("main-image").addEventListener("click", function() {
    this.classList.add("shake");
    setTimeout(() => {
        this.classList.remove("shake");
    }, 500);
});
