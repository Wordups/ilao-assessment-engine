import { expect, test } from "@playwright/test";

test("assessment wizard saves and exposes review content", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Continue as Demo User" }).click();
  await expect(page.getByText("Assessment workspace ready.")).toBeVisible();

  await page.getByLabel("Assessment Title").fill("Playwright Verification Assessment");
  await page.getByLabel("Organization Name").fill("Browser Verification Org");
  await page.getByRole("button", { name: "Next" }).click();

  await page.getByRole("button", { name: "Add Step" }).click();
  await page.getByLabel("Description").fill("Inbound requests are gathered from digital channels.");
  await page.getByLabel("Step Name").fill("Capture online intake");
  await page.getByLabel("Notes").fill("Manual data cleanup still occurs.");
  await page.getByRole("button", { name: "Next" }).click();

  await page.getByRole("button", { name: "Add Step" }).click();
  await page.getByLabel("Description").fill("Rules are checked by the operations team.");
  await page.getByLabel("Step Name").fill("Review eligibility");
  await page.getByLabel("Notes").fill("Policy logic is maintained in spreadsheets.");
  await page.getByRole("button", { name: "Next" }).click();

  await page.getByRole("button", { name: "Add Step" }).click();
  await page.getByLabel("Description").fill("Notifications are partly templated.");
  await page.getByLabel("Step Name").fill("Notify downstream team");
  await page.getByLabel("Notes").fill("Needs integration with the case tool.");
  await page.getByRole("button", { name: "Next" }).click();

  await page.getByRole("button", { name: "Add Step" }).click();
  await page.getByLabel("Description").fill("Weekly metrics are assembled for leadership.");
  await page.getByLabel("Step Name").fill("Prepare leadership report");
  await page.getByLabel("Notes").fill("Formatting is repeated every week.");
  await page.getByRole("button", { name: "Next" }).click();

  await page.getByRole("button", { name: "Save Assessment" }).click();
  await expect(page.getByText("Assessment saved and analyzed.")).toBeVisible();
  const detailPanel = page.locator(".detail-panel");
  await expect(detailPanel.getByRole("heading", { name: "Playwright Verification Assessment" })).toBeVisible();
  await expect(detailPanel.getByRole("heading", { name: "Executive Summary" })).toBeVisible();
  await expect(detailPanel.getByText("Capture online intake", { exact: true })).toBeVisible();
});
