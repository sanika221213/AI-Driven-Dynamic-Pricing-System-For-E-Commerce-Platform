# CHAPTER 3: SYSTEM ANALYSIS

---

## 3.1 REQUIREMENTS ANALYSIS

### 3.1.1 Functional Requirements

The AI-Driven Dynamic Pricing System must satisfy comprehensive functional requirements across multiple user roles and operational scenarios. These requirements define what the system must do to deliver value to its stakeholders.

**FR1: Product Management Requirements**

FR1.1: The system shall allow administrators to create new products with attributes including name, description, category, base price, cost, current stock quantity, and optional image URLs.

FR1.2: The system shall support updating product attributes, including price overrides that temporarily suspend automatic pricing.

FR1.3: The system shall enable bulk product upload via CSV or API endpoints for efficient catalog management.

FR1.4: The system shall maintain complete product lifecycle history including all attribute changes with timestamps.

FR1.5: The system shall support product categorization enabling category-level analytics and pricing strategies.

FR1.6: The system shall allow setting product-specific constraints including minimum price (floor), maximum price (ceiling), and maximum price change rate.

FR1.7: The system shall support product status management (active, discontinued, out-of-stock) affecting availability in customer interfaces.

**FR2: Sales and Transaction Processing**

FR2.1: The system shall record each sale transaction with details including product, quantity, price charged, timestamp, and customer identifier.

FR2.2: The system shall automatically update inventory levels upon sale completion, decrementing stock quantities.

FR2.3: The system shall maintain comprehensive sales history enabling historical analysis and model training.

FR2.4: The system shall support bulk sales import for integrating with external e-commerce platforms or POS systems.

FR2.5: The system shall calculate and track revenue metrics aggregated by product, category, time period, and other dimensions.

FR2.6: The system shall detect and flag anomalous transactions (unusual quantities, prices, or patterns) for review.

**FR3: Demand Forecasting**

FR3.1: The system shall generate demand forecasts for all active products at configurable forecast horizons (default: 7 days ahead).

FR3.2: The system shall utilize LSTM neural network architecture processing historical sales data to identify temporal patterns.

FR3.3: The system shall incorporate external features including day-of-week, month, seasonality indicators, and promotion flags to improve forecast accuracy.

FR3.4: The system shall provide confidence intervals or uncertainty estimates alongside point forecasts.

FR3.5: The system shall support automatic periodic retraining of forecast models as new data accumulates.

FR3.6: The system shall track forecast accuracy metrics (MAE, MAPE, RMSE) enabling model performance monitoring.

FR3.7: The system shall handle cold-start scenarios for new products with limited historical data using baseline methods or transfer learning.

FR3.8: The system shall store forecast history enabling retrospective analysis of prediction accuracy.

**FR4: Price Optimization**

FR4.1: The system shall implement Reinforcement Learning agent that learns optimal pricing policies through interaction with market environment.

FR4.2: The system shall define comprehensive state representation capturing demand levels, inventory status, competitive positioning, seasonality, and trend direction.

FR4.3: The system shall support configurable action spaces defining available price multipliers or absolute price adjustments.

FR4.4: The system shall implement ε-greedy exploration strategy balancing exploration of new prices against exploitation of known good prices.

FR4.5: The system shall compute price elasticity estimates quantifying demand responsiveness to price changes.

FR4.6: The system shall integrate forecasts, RL Q-values, elasticity estimates, and business rules in the Dynamic Pricing Engine to determine optimal prices.

FR4.7: The system shall enforce pricing constraints including price bounds, rate-of-change limits, and strategic positioning requirements.

FR4.8: The system shall support multiple optimization objectives including revenue maximization, profit maximization, and inventory turnover optimization.

FR4.9: The system shall enable manual price overrides with administrative approval, temporarily suspending automatic pricing.

FR4.10: The system shall provide price recommendation explanations detailing factors influencing each pricing decision.

**FR5: Competitor Monitoring**

FR5.1: The system shall maintain database of competitor products with attributes including name, price, website URL, and last update timestamp.

FR5.2: The system shall support manual competitor price entry through administrative interface.

FR5.3: The system shall incorporate competitor price information into pricing decision logic, ensuring competitive positioning.

FR5.4: The system shall track competitor price history enabling analysis of competitive dynamics over time.

FR5.5: The system shall detect and alert on significant competitor price changes exceeding configurable thresholds.

FR5.6: The system shall support mapping of competitor products to internal products for direct comparison.

**FR6: Customer Shopping Experience**

FR6.1: The system shall provide customer-facing interface displaying all available products with current prices.

FR6.2: The system shall support product search and filtering by category, price range, and keywords.

FR6.3: The system shall enable customers to add products to shopping cart and adjust quantities.

FR6.4: The system shall calculate cart totals including subtotal and (if implemented) taxes and shipping.

FR6.5: The system shall support checkout process capturing customer information and finalizing sales.

FR6.6: The system shall optionally display price history or comparisons if transparency strategy calls for it.

FR6.7: The system shall ensure price consistency—price presented when product is added to cart remains locked until checkout or configurable timeout.

**FR7: Analytics and Reporting**

FR7.1: The system shall provide administrative dashboard displaying KPIs including total revenue, sales volume, average order value, active products, and conversion rates.

FR7.2: The system shall generate time-series visualizations of revenue trends, sales patterns, and pricing evolution.

FR7.3: The system shall produce product-level performance reports comparing forecasts to actuals and tracking pricing effectiveness.

FR7.4: The system shall enable comparative analysis showing performance under dynamic vs. static pricing scenarios.

FR7.5: The system shall provide drill-down capabilities exploring aggregated metrics by time period, product, category, or other dimensions.

FR7.6: The system shall support export of analytics data in CSV, JSON, or Excel formats for external analysis.

FR7.7: The system shall maintain performance metrics tracking system health including API response times, model prediction latencies, and database query performance.

**FR8: User Authentication and Authorization**

FR8.1: The system shall implement user authentication requiring username and password for access to administrative functions.

FR8.2: The system shall support multiple user roles including administrator (full access), pricing manager (pricing controls only), and analyst (read-only analytics access).

FR8.3: The system shall maintain user session management with configurable timeout policies.

FR8.4: The system shall log all administrative actions including product modifications and price overrides for audit trails.

FR8.5: The system shall protect sensitive operations with authorization checks ensuring only privileged users can execute them.

**FR9: System Configuration**

FR9.1: The system shall provide configuration interface for setting global parameters including default price bounds, RL hyperparameters, forecast update frequency, and pricing strategy selection.

FR9.2: The system shall support both global configuration and product-specific overrides enabling flexible customization.

FR9.3: The system shall validate all configuration changes ensuring parameter values remain within acceptable ranges.

FR9.4: The system shall track configuration history enabling rollback to previous settings if needed.

FR9.5: The system shall support A/B testing framework allowing controlled experiments comparing different pricing strategies.

### 3.1.2 Non-Functional Requirements

Beyond functional capabilities, the system must satisfy quality attributes ensuring it operates effectively in production environments.

**NFR1: Performance**

NFR1.1: API endpoints shall respond within 200 milliseconds for 95% of requests under normal load (100 concurrent users).

NFR1.2: Price optimization for individual products shall complete within 5 seconds.

NFR1.3: Batch price optimization across entire product catalog shall complete within 15 minutes for catalogs up to 10,000 products.

NFR1.4: Demand forecast generation shall process all products within 30 minutes when run daily.

NFR1.5: Database queries supporting dashboard visualizations shall execute within 1 second.

NFR1.6: System shall support minimum 100 transactions per second throughput during peak load.

**NFR2: Scalability**

NFR2.1: System architecture shall support horizontal scaling, enabling addition of API server instances to handle increased load.

NFR2.2: Database design shall accommodate growth to 100,000 products and 10 million historical sales records without performance degradation.

NFR2.3: Machine learning model training shall utilize available GPU acceleration when hardware supports it.

NFR2.4: System shall gracefully handle catalog expansions, with computational complexity growing linearly or sublinearly with product count.

**NFR3: Reliability and Availability**

NFR3.1: System shall achieve 99.5% uptime during business-critical hours (defined by business requirements).

NFR3.2: Automated health checks shall monitor system components every 60 seconds, triggering alerts on failures.

NFR3.3: Database transactions shall be ACID-compliant ensuring data integrity under concurrent access and failure scenarios.

NFR3.4: System shall implement comprehensive error handling preventing crashes from malformed inputs, data anomalies, or transient failures.

NFR3.5: Automated backup processes shall capture database snapshots daily, retained for 30 days.

NFR3.6: System shall implement graceful degradation—if ML components fail, fallback to rule-based pricing prevents complete service interruption.

**NFR4: Security**

NFR4.1: All authentication credentials shall be stored using strong cryptographic hashing (bcrypt or equivalent).

NFR4.2: API endpoints modifying data shall require authentication and validate user authorization.

NFR4.3: System shall protect against common web vulnerabilities including SQL injection, XSS, and CSRF per OWASP Top 10.

NFR4.4: Sensitive data (costs, profit margins) shall be accessible only to authorized users.

NFR4.5: System shall implement rate limiting preventing abuse through excessive API requests.

NFR4.6: All communications shall support HTTPS/TLS encryption when deployed in production.

NFR4.7: Audit logs shall record all administrative actions with user, timestamp, and action details.

**NFR5: Usability**

NFR5.1: Administrative interfaces shall follow intuitive design principles enabling users to accomplish common tasks without training.

NFR5.2: System shall provide informative error messages guiding users toward resolution rather than generic failures.

NFR5.3: Interfaces shall be responsive, adapting to different screen sizes (desktop, tablet, mobile).

NFR5.4: Data visualizations shall clearly communicate information using appropriate chart types, legends, and labels.

NFR5.5: System shall provide contextual help documentation accessible from relevant interface sections.

**NFR6: Maintainability**

NFR6.1: Code shall follow PEP 8 style guidelines for Python ensuring consistency and readability.

NFR6.2: All modules shall include comprehensive docstrings documenting purpose, parameters, return values, and exceptions.

NFR6.3: System architecture shall be modular enabling independent development, testing, and replacement of components.

NFR6.4: Configuration shall be externalized from code enabling adjustments without code changes.

NFR6.5: Database schema shall support migrations enabling structure evolution without data loss.

NFR6.6: Comprehensive logging shall record significant events, errors, and decision rationales supporting troubleshooting.

**NFR7: Testability**

NFR7.1: System architecture shall support unit testing of individual components in isolation.

NFR7.2: API endpoints shall include test coverage verifying correct behavior under normal and edge case inputs.

NFR7.3: Mock data generation capabilities shall support testing without requiring production data access.

NFR7.4: System shall support test environments separate from production enabling safe experimentation.

**NFR8: Interoperability**

NFR8.1: API shall follow REST principles using standard HTTP methods and JSON serialization.

NFR8.2: Database shall support migration to enterprise databases (PostgreSQL, MySQL) beyond development SQLite.

NFR8.3: System shall support data export in standard formats (CSV, JSON) enabling integration with external tools.

NFR8.4: Time stamps shall use ISO 8601 format and UTC timezone enabling global interoperability.

**NFR9: Portability**

NFR9.1: System shall run on Windows, macOS, and Linux operating systems without modification.

NFR9.2: Dependencies shall be documented with version constraints enabling reproducible deployment.

NFR9.3: System shall support containerization (Docker) for consistent deployment across environments.

**NFR10: Compliance and Ethics**

NFR10.1: System shall maintain transparent pricing logic avoiding discriminatory pricing based on protected characteristics.

NFR10.2: Price changes shall be logged enabling regulatory audit if required.

NFR10.3: Customer data handling shall follow privacy best practices with minimal collection and secure storage.

NFR10.4: System shall support configurable pricing constraints preventing potentially harmful pricing (e.g., excessive surge pricing for essential goods).

## 3.2 FEASIBILITY ANALYSIS

### 3.2.1 Technical Feasibility

**Assessment:** The proposed system is technically feasible using established technologies and methods.

**Supporting Evidence:**
- Python, Flask, SQLite, TensorFlow, NumPy are mature technologies with extensive documentation and community support
- LSTM for demand forecasting has been successfully applied in similar retail contexts (Wen et al., 2017)
- Q-Learning for pricing has been validated in academic research and limited commercial deployments
- REST APIs and web-based interfaces are standard approaches with well-understood implementation patterns
- Development team has access to necessary computational resources (standard CPU/GPU-equipped workstations sufficient for prototype and demonstration)

**Risks and Mitigation:**
- *Risk:* LSTM training may require substantial data; early products lack sufficient history
- *Mitigation:* Implement baseline forecasting methods for cold-start scenarios; use synthetic data generation for initial testing

- *Risk:* RL exploration may initially recommend suboptimal prices before learning converges
- *Mitigation:* Initialize Q-values using heuristics; implement price bounds and rate limits; allow manual override

- *Risk:* Real-time performance requirements may not be met under high load
- *Mitigation:* Implement caching for frequently accessed data; use asynchronous processing for heavy computations; profile and optimize bottlenecks

**Conclusion:** Technical feasibility is high. While challenges exist, they are addressable through standard engineering practices.

### 3.2.2 Economic Feasibility

**Assessment:** The system is economically viable with modest development costs and significant potential returns.

**Development Costs:**
- Personnel: Primary development by student/small team (limited direct cost in academic context)
- Software: All dependencies are open-source (zero licensing costs)
- Hardware: Standard development workstations (no additional cost)
- Data: Synthetic data generation for prototype; real deployment would use business's existing sales data (no additional data acquisition costs)
- Infrastructure: Cloud hosting costs minimal for prototype scale ($50-200/month depending on scale)

**Total Estimated Development Cost:** Minimal in academic context; approximately $5,000-15,000 if commercial development (primarily personnel time)

**Expected Benefits:**
- Revenue improvement from dynamic pricing: Research suggests 10-25% revenue gains vs. static pricing
- For typical e-commerce business with $1M annual revenue, even 10% improvement represents $100K additional annual revenue
- Improved inventory management reducing holding costs and stockouts
- Competitive positioning improvements
- Data-driven decision making replacing manual guesswork

**Return on Investment:**
- For commercial deployment, payback period likely <3 months given modest development costs and substantial revenue potential
- Ongoing operational costs minimal (server hosting, periodic maintenance)

**Conclusion:** Economic feasibility is excellent. Benefits substantially outweigh costs, particularly for e-commerce businesses with reasonable scale.

### 3.2.3 Operational Feasibility

**Assessment:** The system can be effectively deployed and integrated into business operations with appropriate change management.

**Integration Considerations:**
- System designed to integrate with existing e-commerce platforms via API
- Database can ingest sales data from external systems
- Pricing decisions can feed back to product management systems

**Organizational Requirements:**
- Pricing managers must understand dynamic pricing principles and trust algorithmic recommendations
- IT staff must support deployment and maintenance
- Marketing/customer service teams must communicate pricing strategy to customers if needed

**Change Management:**
- Gradual rollout allows validation before full deployment
- Manual override capabilities maintain human control
- Training and documentation support adoption
- Clear explanation of pricing decisions builds trust

**Risk Factors:**
- Resistance to algorithmic pricing from managers accustomed to manual control
- Customer confusion or backlash if pricing changes are too frequent or extreme
- Competitive response to pricing changes

**Mitigation Strategies:**
- Demonstrate system value through pilot programs on subset of products
- Maintain transparency about pricing logic
- Implement safeguards limiting pricing volatility
- Monitor customer feedback and competitive responses

**Conclusion:** Operational feasibility is moderate to high. Success depends on effective change management and stakeholder buy-in beyond pure technical implementation.

### 3.2.4 Legal and Ethical Feasibility

**Assessment:** The system can be deployed in ethically and legally compliant manner with appropriate safeguards.

**Legal Considerations:**
- Algorithmic pricing is legal in most jurisdictions when practiced fairly
- Price discrimination based on protected characteristics (race, gender, etc.) is prohibited and must be avoided
- Some industries (e.g., healthcare, utilities) face price regulation requiring compliance
- Antitrust laws prohibit collusion; algorithmic pricing must not facilitate tacit collusion
- Consumer protection laws in some regions may require price transparency

**Ethical Considerations:**
- Dynamic pricing can be perceived as unfair if extreme or opaque
- Surge pricing for essential goods during emergencies raises ethical concerns
- Personalized pricing based on individual customer data sensitivity controversial
- Transparency vs. complexity trade-off—customers may prefer knowing why prices change

**System Design for Compliance:**
- Product-level pricing (not individual customer personalization) avoids discrimination concerns
- Configurable price bounds and limits prevent extreme pricing
- Audit logging supports regulatory compliance
- Transparency features can be enabled if desired
- Manual oversight maintains human accountability

**Conclusion:** Legal and ethical feasibility is high provided system is configured with appropriate constraints and oversight. Product-level dynamic pricing avoiding individual discrimination represents the sweet spot of effectiveness and acceptability.

### 3.2.5 Schedule Feasibility

**Assessment:** System can be developed within academic project timeline (typically 4-6 months).

**Development Phases:**

Phase 1 (Weeks 1-4): Requirements and Design
- Detailed requirements specification
- System architecture design
- Database schema design
- Technology selection and setup

Phase 2 (Weeks 5-8): Core Infrastructure
- Database implementation
- API framework setup
- Basic CRUD operations
- Authentication system

Phase 3 (Weeks 9-12): ML Components
- LSTM demand forecasting implementation and training
- Q-Learning RL agent implementation
- Price elasticity calculator
- Initial model validation

Phase 4 (Weeks 13-16): Integration and Frontend
- Dynamic Pricing Engine integration
- Frontend interface development
- End-to-end workflow testing
- Performance optimization

Phase 5 (Weeks 17-20): Testing and Documentation
- Comprehensive testing
- Documentation completion
- Demonstration preparation
- Final refinements

**Critical Path:** ML component development represents longest dependency chain. Parallel development of infrastructure and frontend where possible.

**Risk Factors:**
- Model training may require more iterations than anticipated
- Integration challenges between components
- Performance issues requiring optimization
- Scope creep expanding requirements

**Mitigation:**
- Prioritize core features; defer nice-to-have enhancements
- Regular testing of integrated system components
- Buffer time in schedule for unexpected issues
- Strict scope management

**Conclusion:** Schedule feasibility is good with disciplined project management. Timeline is ambitious but achievable for focused development effort.

## 3.3 CURRENT SYSTEM ANALYSIS

Most e-commerce businesses currently use one of several pricing approaches:

### 3.3.1 Static Cost-Plus Pricing

**Approach:** Set prices at fixed markup over cost (e.g., cost + 40%)

**Advantages:**
- Simple to implement and understand
- Ensures minimum margin maintained
- Minimal computational requirements

**Limitations:**
- Ignores market conditions and demand
- Cannot respond to competitive changes
- Misses revenue optimization opportunities
- Same markup applied regardless of product's demand elasticity

**Prevalence:** Common among small retailers and businesses with limited analytical capabilities

### 3.3.2 Manual Competitive Pricing

**Approach:** Managers periodically check competitor prices and adjust to match or undercut

**Advantages:**
- Considers competitive positioning
- Allows human judgment and strategic thinking
- Flexible to special circumstances

**Limitations:**
- Labor-intensive and scales poorly with catalog size
- Delayed response to market changes
- Inconsistent—depends on manager availability and diligence
- Reactive rather than proactive
- Vulnerable to price wars

**Prevalence:** Common among online retailers competing in transparent markets

### 3.3.3 Rule-Based Automated Pricing

**Approach:** Simple rules automatically adjust prices (e.g., "price 5% below lowest competitor")

**Advantages:**
- Automated, reducing manual effort
- Rapid response to trigger conditions
- Consistent application of rules
- Scalable to large catalogs

**Limitations:**
- Rules often simplistic, not capturing complex tradeoffs
- No learning or adaptation—same rules applied forever
- Can trigger destructive price wars when competing algorithms interact
- No demand forecasting—cannot anticipate future conditions
- Difficult to encode complex strategies in rule form

**Prevalence:** Used by sophisticated online retailers and marketplace sellers (e.g., Amazon third-party sellers using repricing software)

### 3.3.4 Limitations of Current Approaches

**Lack of Demand Intelligence:**
None of the traditional approaches incorporate demand forecasting. Pricing decisions are made without understanding how demand will evolve, missing opportunities to premium price during demand peaks or discount during troughs.

**No Learning:**
Traditional systems don't improve from experience. Mistakes are repeated; successful strategies aren't reinforced.

**Incomplete Optimization:**
Current systems optimize at most one factor (cost coverage, competitive positioning) rather than holistically balancing multiple objectives.

**Scale Constraints:**
Manual approaches don't scale to large catalogs. Automated rules scale but remain simplistic.

**Strategic Limitations:**
Current systems don't think ahead—they react to immediate conditions without considering how today's prices affect tomorrow's competitive position or customer relationships.

**Data Underutilization:**
Most businesses collect rich data on sales, customer behavior, and market conditions but use only small fractions of this information for pricing.

### 3.3.5 The Need for AI-Driven Solutions

The limitations of current systems create compelling case for AI-driven dynamic pricing:

**Forecasting:** ML models can extract patterns from historical data to predict future demand

**Learning:** RL agents improve pricing policies through experience

**Optimization:** Integration of forecasting, elasticity, and optimization enables holistic decision-making

**Scalability:** Once developed, ML systems scale to large catalogs with minimal marginal cost

**Adaptability:** Models continuously update as conditions change

**Data Utilization:** Advanced algorithms can leverage all available data, converting it from passive records into active intelligence

This analysis establishes that while current approaches have served businesses adequately, substantial opportunities exist for improvement through intelligent, data-driven pricing—opportunities that our proposed system aims to capture.

## 3.4 PROPOSED SYSTEM ADVANTAGES

The AI-driven dynamic pricing system offers substantial advantages over current approaches:

**Advantage 1: Data-Driven Demand Intelligence**
- LSTM forecasting provides 7-day demand predictions with quantified confidence
- Forecasts incorporate seasonality, trends, and external factors ignored by simple heuristics
- Enables proactive pricing anticipating demand shifts rather than reacting after they occur

**Advantage 2: Continuous Learning and Improvement**
- RL agent learns from outcomes, improving pricing policy over time
- Q-values updated with each transaction, incorporating latest market feedback
- System gets smarter with experience rather than remaining static

**Advantage 3: Multi-Objective Optimization**
- Balances revenue, profit, inventory, and competitive positioning simultaneously
- Configurable to prioritize objectives matching business strategy
- Avoids sub-optimization of single metric at expense of others

**Advantage 4: Scalability**
- Automated processing handles thousands of products efficiently
- Marginal cost of pricing additional products is minimal once system developed
- Consistent application of sophisticated logic across entire catalog

**Advantage 5: Speed and Responsiveness**
- Real-time pricing updates respond to market changes within minutes
- API-based architecture enables integration with live inventory and competitor data feeds
- Eliminates delays inherent in manual processes

**Advantage 6: Transparency and Explainability**
- System provides detailed rationale for each pricing decision
- Administrators can understand why prices changed
- Builds trust and enables human oversight

**Advantage 7: Flexibility and Configurability**
- Product-specific constraints accommodate special cases
- Manual overrides maintain human control when needed
- A/B testing framework supports controlled experimentation

**Advantage 8: Safety and Risk Management**
- Price bounds and rate limits prevent extreme pricing errors
- Fallback mechanisms maintain operation even if ML components fail
- Audit logging tracks all decisions enabling review

**Advantage 9: Competitive Intelligence Integration**
- Considers competitor prices in optimization
- Avoids destructive price wars through intelligent response rather than blind matching
- Maintains strategic positioning while remaining competitive

**Advantage 10: Inventory Optimization Integration**
- Pricing accounts for inventory levels, moderating demand when stock is low and accelerating turnover when excess exists
- Coordinates pricing and inventory management for overall business optimization

**Quantified Expected Improvements:**

Based on academic literature and industry benchmarks:

- Revenue: 10-25% increase vs. static pricing
- Profit margin: 3-8% improvement through better cost recovery and optimization
- Inventory turnover: 15-20% faster through pricing-driven demand management
- Price optimization time: 90%+ reduction in manual effort
- Forecast accuracy: 15-30% MAPE (vs. 30-50% for naive baselines)
- Decision speed: Real-time (seconds) vs. hours/days for manual analysis

These advantages collectively represent substantial value proposition, particularly for e-commerce businesses operating in competitive, dynamic markets with large product catalogs.

---

**END OF CHAPTER 3**

*Total Word Count: ~5,500 words*

This extended System Analysis chapter provides comprehensive coverage of requirements (functional and non-functional), feasibility analysis across multiple dimensions, current system limitations, and proposed system advantages.
