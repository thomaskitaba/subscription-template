var newsletter = document.getElementById("newsletter");
newsletter_duration = document.getElementById("newsletter-duration");
var newsletter_subscription;
function show(){
  console.log("Thomas Kitaba");
    newsletter_subscription = newsletter.value;
  console.log(newsletter_subscription);
  if (newsletter_subscription == "Yes")
  {
    newsletter_duration.style.display = "block";
  }
  else
  {
    newsletter_duration.style.display = "none";
  }
}

