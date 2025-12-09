// GBS Homepage - JavaScript

// CTA Button Event Listener
document.addEventListener("DOMContentLoaded", () => {
  const ctaButton = document.getElementById("ctaButton")

  if (ctaButton) {
    ctaButton.addEventListener("click", handleCtaClick)
  }
})

/**
 * Handle CTA button click
 * Future hook for SIRET eligibility check
 */
function handleCtaClick() {
  console.log("[GBS] CTA button clicked - Ready for SIRET eligibility check")

  // TODO: Implement SIRET eligibility check
  // This function will:
  // 1. Open a modal or navigate to an eligibility form
  // 2. Accept SIRET input
  // 3. Validate and check eligibility
  // 4. Display results
}

/**
 * Future function: Check SIRET eligibility
 * @param {string} siret - The SIRET number to check
 * @returns {Promise<Object>} - Eligibility result
 */
async function checkSiretEligibility(siret) {
  try {
    console.log(`[GBS] Checking SIRET eligibility: ${siret}`)
    // TODO: Make API call to eligibility check endpoint
    // const response = await fetch('/api/check-eligibility', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ siret })
    // });
    // return await response.json();
  } catch (error) {
    console.error("[GBS] Error checking SIRET:", error)
    throw error
  }
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  })
})
