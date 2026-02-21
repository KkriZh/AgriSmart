const regionFactor = {
  temperate: 1.0,
  arid: 1.35,
  tropical: 1.2,
  coastal: 1.1,
  highland: 0.9,
};

const seasonFactor = {
  spring: 1.0,
  summer: 1.25,
  monsoon: 0.75,
  autumn: 0.9,
  winter: 0.85,
};

const cropFactor = {
  grains: 1.05,
  vegetables: 1.3,
  legumes: 0.9,
  fruit: 1.2,
};

const fertilizerFocus = {
  grains: "Nitrogen + balanced blend",
  vegetables: "Nitrogen + potassium",
  legumes: "Phosphorus + calcium",
  fruit: "Potassium + micronutrients",
};

const baseDays = {
  grains: 120,
  vegetables: 75,
  legumes: 90,
  fruit: 180,
};

const laborBase = {
  grains: 2,
  vegetables: 3,
  legumes: 2,
  fruit: 3,
};

const form = document.getElementById("planner-form");
const regionInput = document.getElementById("region");
const seasonInput = document.getElementById("season");
const cropInput = document.getElementById("crop");
const landInput = document.getElementById("land");

const waterOutput = document.getElementById("water-cadence");
const fertilizerOutput = document.getElementById("fertilizer-focus");
const harvestOutput = document.getElementById("harvest-window");
const laborOutput = document.getElementById("labor-intensity");

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function computePlan() {
  const region = regionInput.value;
  const season = seasonInput.value;
  const crop = cropInput.value;
  const land = clamp(parseFloat(landInput.value) || 1, 1, 2000);

  const cadence = Math.max(
    2,
    Math.round(3.1 * regionFactor[region] * seasonFactor[season] * cropFactor[crop])
  );

  const centerDays = Math.round(baseDays[crop] * seasonFactor[season]);
  const minDays = Math.max(45, centerDays - 6);
  const maxDays = centerDays + 8;

  const laborScore = laborBase[crop] + (land > 150 ? 2 : land > 60 ? 1 : 0);
  const laborLabel = laborScore >= 4 ? "High" : laborScore >= 3 ? "Moderate" : "Light";

  waterOutput.textContent = `${cadence}x per week`;
  fertilizerOutput.textContent = fertilizerFocus[crop];
  harvestOutput.textContent = `${minDays}-${maxDays} days`;
  laborOutput.textContent = laborLabel;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  computePlan();
});

[regionInput, seasonInput, cropInput].forEach((input) => {
  input.addEventListener("change", computePlan);
});

landInput.addEventListener("input", computePlan);

document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("loaded");
  computePlan();

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const targetId = link.getAttribute("href");
      if (!targetId || targetId === "#") {
        return;
      }
      const target = document.querySelector(targetId);
      if (!target) {
        return;
      }
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
