#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Typing effect
type_text() {
  text="$1"
  for (( i=0; i<${#text}; i++ )); do
    echo -n "${text:$i:1}"
    sleep 0.02
  done
  echo ""
}

clear

# 🔀 PR CONTEXT
echo -e "${BLUE}----------------------------------------------"
echo "🔀 Pull Request: #42 - Drop user_id column"
echo "👤 Author: yashpawarrr"
echo "📁 Files changed: models/orders.sql"
echo -e "----------------------------------------------${NC}"
sleep 2

type_text "🚀 Starting OpenMetadata Data Governance Suite Demo..."
sleep 1

# 📂 DETECTION
type_text "📂 Detecting SQL changes in Pull Request..."
sleep 2
type_text "✔ Found change: ${RED}DROP COLUMN user_id FROM orders${NC}"
sleep 2

# 📝 SQL DIFF
echo ""
echo -e "${YELLOW}📝 SQL Diff:${NC}"
echo "- SELECT user_id, order_id FROM orders;"
echo "+ SELECT order_id FROM orders;"
sleep 2

# 🔍 LINEAGE
type_text ""
type_text "🔍 Fetching lineage from OpenMetadata API..."
sleep 2
echo -e "${GREEN}✔ Downstream Impact:${NC}"
echo "   - Tables: user_activity, revenue_summary, customer_360"
echo "   - Dashboards: Revenue Dashboard, User Funnel"
sleep 3

# 📜 CONTRACT
type_text ""
type_text "📜 Validating Data Contracts..."
sleep 2
echo -e "${RED}❌ VIOLATION: Column 'user_id' is REQUIRED by contract${NC}"
echo -e "${YELLOW}💡 Suggested Fix: Update contract or avoid dropping column${NC}"
sleep 3

# ⚠️ QUALITY
type_text ""
type_text "⚠️ Running Data Quality Checks..."
sleep 2
echo -e "${YELLOW}⚠️ WARNING: Table 'orders' quality score = 0.62${NC}"
sleep 2

# 💰 COST
type_text ""
type_text "💰 Estimating Query Cost..."
sleep 2
echo -e "${GREEN}💸 Estimated full-scan cost:${NC}"
echo "   Table Size: 500 GB"
echo "   Scan Cost Model: \$5 / TB"
echo -e "   👉 Estimated Cost: ${GREEN}\$12.50${NC}"
sleep 3

# 🔔 SLACK
type_text ""
type_text "📢 Sending Slack Notification..."
sleep 2
echo -e "${GREEN}✔ Slack alert sent${NC}"
echo ""
echo "💬 Slack Preview:"
echo "📊 OpenMetadata Alert"
echo "⚠️ Breaking change in 'orders'"
echo "🔻 3 tables | 2 dashboards affected"
echo "💸 Cost: \$12.50"
echo "🔗 github.com/pr/42"
sleep 3

# 🧠 AI REPORT
type_text ""
type_text "🧠 Generating AI Impact Report..."
sleep 2

echo ""
echo -e "${BLUE}=============================================="
echo "📋 OpenMetadata Governance Report"
echo -e "==============================================${NC}"
echo ""
echo -e "${RED}❌ Breaking Change Detected${NC}"
echo "   Column 'user_id' dropped from 'orders'"
echo ""
echo -e "${YELLOW}🔻 Impact:${NC}"
echo "   - 3 downstream tables affected"
echo "   - 2 dashboards impacted"
echo ""
echo -e "${YELLOW}💡 Suggested Fix:${NC}"
echo "   Update joins in user_activity model"
echo ""
echo -e "${BLUE}==============================================${NC}"

# 🤖 AI INSIGHT
echo ""
echo -e "${BLUE}🤖 AI Insight:${NC}"
type_text "Dropping 'user_id' will break critical joins in downstream analytics models."
type_text "Recommended approach: deprecate column and migrate dependencies gradually."
sleep 2

# ❌ FINAL END
echo ""
type_text "❌ CI STATUS: FAILED (Blocking Merge)"
echo ""
type_text "🚫 Merge prevented to protect downstream systems."
sleep 2

echo ""
type_text "✨ Demo Completed Successfully!"
echo ""

exit 0
