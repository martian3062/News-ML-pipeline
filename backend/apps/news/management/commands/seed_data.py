"""
Seed demo data — categories, articles, story arcs, briefings, users.
Usage: python manage.py seed_data
"""

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


CATEGORIES = [
    {"name": "Markets", "slug": "markets", "icon": "📈", "color": "#10b981"},
    {"name": "Startups", "slug": "startups", "icon": "🚀", "color": "#8b5cf6"},
    {"name": "Technology", "slug": "technology", "icon": "💻", "color": "#3b82f6"},
    {"name": "Economy", "slug": "economy", "icon": "🏛️", "color": "#f59e0b"},
    {"name": "Finance", "slug": "finance", "icon": "💰", "color": "#06b6d4"},
    {"name": "World", "slug": "world", "icon": "🌍", "color": "#ef4444"},
    {"name": "AI & ML", "slug": "ai-ml", "icon": "🤖", "color": "#ec4899"},
    {"name": "Energy", "slug": "energy", "icon": "⚡", "color": "#84cc16"},
]


ARTICLES = [
    {
        "title": "Sensex Rallies 800 Points as FII Inflows Surge to Record High",
        "content": (
            "Indian equity markets staged a powerful rally on Monday with the BSE Sensex surging over 800 points, "
            "driven by a massive wave of foreign institutional investor inflows. The benchmark index closed at 78,450, "
            "its highest level in three months, as FIIs poured in ₹12,500 crore in a single trading session.\n\n"
            "Banking and IT stocks led the charge, with HDFC Bank gaining 3.2% and Infosys rising 2.8%. Market analysts "
            "attribute the rally to improving global sentiment following the US Federal Reserve's dovish stance on interest rates.\n\n"
            "\"This is one of the strongest single-day FII inflows we've seen in 2026,\" said Rajesh Mehta, Chief Market "
            "Strategist at ICICI Securities. \"The combination of attractive valuations, a weakening dollar, and India's "
            "strong GDP growth trajectory is making Indian equities irresistible for global investors.\"\n\n"
            "Small and mid-cap indices also participated in the rally, with the BSE Small Cap index gaining 1.8%. "
            "The India VIX, a measure of market volatility, dropped 12% to its lowest level in six months."
        ),
        "summary": "Sensex surges 800+ points on record FII inflows of ₹12,500 crore, led by banking and IT stocks.",
        "category_slug": "markets",
        "author": "Priya Sharma",
        "source_name": "ET Markets",
        "tags": ["sensex", "FII", "rally", "banking", "IT"],
        "entities": ["BSE Sensex", "HDFC Bank", "Infosys", "ICICI Securities", "US Federal Reserve"],
        "sentiment_score": 0.85,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": True,
        "image_url": "https://images.pexels.com/photos/6801648/pexels-photo-6801648.jpeg?w=800",
    },
    {
        "title": "India's AI Startup Ecosystem Crosses $25 Billion Valuation Mark",
        "content": (
            "India's artificial intelligence startup ecosystem has crossed a landmark $25 billion valuation, "
            "cementing the country's position as a global AI hub. A new report by NASSCOM in partnership with "
            "McKinsey reveals that over 3,200 AI startups are now operational across India, with Bengaluru, "
            "Hyderabad, and Delhi NCR emerging as the top clusters.\n\n"
            "Generative AI companies alone have raised $4.2 billion in funding over the past 18 months, "
            "with enterprises like Krutrim, Sarvam AI, and Ola's AI division leading the charge. The report "
            "highlights that Indian AI startups are increasingly focusing on vertical solutions — healthcare "
            "diagnostics, agricultural yield prediction, and vernacular language processing.\n\n"
            "\"India has moved from being an AI consumer to an AI creator,\" said Debjani Ghosh, President of "
            "NASSCOM. \"The talent pool, combined with the sheer scale of India's data diversity, gives our "
            "startups a unique competitive advantage.\"\n\n"
            "The government's ₹10,000 crore IndiaAI Mission is expected to further accelerate this growth, "
            "with plans to establish 10,000 GPU computing capacity by 2027."
        ),
        "summary": "India's AI startup ecosystem surpasses $25B valuation with 3,200+ startups, led by GenAI companies.",
        "category_slug": "startups",
        "author": "Vikram Patel",
        "source_name": "ET Startups",
        "tags": ["AI", "startups", "NASSCOM", "generative-AI", "funding"],
        "entities": ["NASSCOM", "McKinsey", "Krutrim", "Sarvam AI", "IndiaAI Mission"],
        "sentiment_score": 0.9,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?w=800",
    },
    {
        "title": "RBI Holds Repo Rate Steady at 6.0%, Signals Accommodative Stance",
        "content": (
            "The Reserve Bank of India maintained its benchmark repo rate at 6.0% for the second consecutive "
            "policy meeting, while signaling a shift to an accommodative monetary policy stance. RBI Governor "
            "Sanjay Malhotra cited easing inflation and the need to support economic growth as key factors behind "
            "the decision.\n\n"
            "Consumer inflation has moderated to 4.2%, well within the RBI's target band of 2-6%, while core "
            "inflation remains at a multi-year low of 3.8%. The central bank revised its GDP growth forecast "
            "for FY27 upward to 6.8% from the earlier estimate of 6.5%.\n\n"
            "\"The MPC unanimously decided to keep the repo rate unchanged, but I want to emphasize that the "
            "change in stance to accommodative signals our readiness to support growth,\" Governor Malhotra said "
            "in his post-policy press conference.\n\n"
            "Bond markets reacted positively, with the 10-year government bond yield falling 8 basis points "
            "to 6.72%. Banking stocks also gained, with expectations of improved credit growth in the coming quarters."
        ),
        "summary": "RBI holds repo rate at 6.0%, shifts to accommodative stance. GDP forecast raised to 6.8%.",
        "category_slug": "economy",
        "author": "Ananya Iyer",
        "source_name": "ET Economy",
        "tags": ["RBI", "repo-rate", "monetary-policy", "GDP", "inflation"],
        "entities": ["Reserve Bank of India", "Sanjay Malhotra", "MPC"],
        "sentiment_score": 0.6,
        "reading_level": "advanced",
        "is_trending": True,
        "is_breaking": True,
        "image_url": "https://images.pexels.com/photos/4386476/pexels-photo-4386476.jpeg?w=800",
    },
    {
        "title": "Google Launches Gemini 3.0 Ultra with Real-Time Reasoning Capabilities",
        "content": (
            "Google has unveiled Gemini 3.0 Ultra, its most advanced AI model to date, featuring real-time "
            "reasoning capabilities that can solve complex multi-step problems while explaining its thought "
            "process. The launch positions Google firmly in competition with OpenAI's GPT-5 and Anthropic's "
            "Claude Opus models.\n\n"
            "Key highlights include a 2-million-token context window, native multimodal understanding across "
            "text, images, video, and code, and a new 'reasoning trace' feature that shows users how the model "
            "arrives at its conclusions. Benchmark results show Gemini 3.0 Ultra achieving 92.4% on the GPQA "
            "Diamond benchmark and 88.7% on MATH-500.\n\n"
            "\"Gemini 3.0 Ultra represents a fundamental shift in how AI systems think,\" said Sundar Pichai, "
            "CEO of Alphabet. \"We're not just making models bigger — we're making them think more carefully.\"\n\n"
            "The model is available through Google AI Studio and Vertex AI, with enterprise pricing starting "
            "at $0.00375 per 1K input tokens. Google also announced that Gemini 3.0 Flash, a faster and cheaper "
            "variant, will be available within two weeks."
        ),
        "summary": "Google's Gemini 3.0 Ultra features 2M token context, real-time reasoning traces, and 92.4% GPQA score.",
        "category_slug": "technology",
        "author": "Rohit Kumar",
        "source_name": "ET Tech",
        "tags": ["Google", "Gemini", "AI", "LLM", "reasoning"],
        "entities": ["Google", "Gemini 3.0 Ultra", "Sundar Pichai", "Alphabet", "OpenAI", "Anthropic"],
        "sentiment_score": 0.8,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/17483868/pexels-photo-17483868.jpeg?w=800",
    },
    {
        "title": "India's UPI Transactions Cross 20 Billion Monthly Milestone",
        "content": (
            "India's Unified Payments Interface has achieved a historic milestone, processing over 20 billion "
            "transactions in a single month for the first time. The total transaction value reached ₹22.5 lakh "
            "crore, underscoring India's position as the global leader in real-time digital payments.\n\n"
            "PhonePe maintained its market leadership with a 47% share, followed by Google Pay at 35% and "
            "Paytm at 8%. The NPCI credited the growth to expansion in Tier-3 and Tier-4 cities, where UPI "
            "adoption has grown 65% year-on-year.\n\n"
            "\"The democratization of digital payments is transforming India's economy from the ground up,\" "
            "said Dilip Asbe, CEO of NPCI. \"We're seeing street vendors, auto-rickshaw drivers, and small "
            "farmers all embracing UPI as their primary payment method.\"\n\n"
            "UPI's international expansion also continues, with the platform now live in Singapore, UAE, France, "
            "and Sri Lanka. NPCI International is in talks with 15 more countries for UPI integration."
        ),
        "summary": "UPI hits 20 billion monthly transactions — ₹22.5 lakh crore value. PhonePe leads with 47% share.",
        "category_slug": "finance",
        "author": "Deepa Nair",
        "source_name": "ET Finance",
        "tags": ["UPI", "digital-payments", "fintech", "NPCI", "PhonePe"],
        "entities": ["UPI", "PhonePe", "Google Pay", "Paytm", "NPCI", "Dilip Asbe"],
        "sentiment_score": 0.88,
        "reading_level": "beginner",
        "is_trending": False,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/4386431/pexels-photo-4386431.jpeg?w=800",
    },
    {
        "title": "ISRO Successfully Tests Reusable Launch Vehicle in Orbital Return Mission",
        "content": (
            "The Indian Space Research Organisation has successfully completed the orbital return mission of its "
            "Reusable Launch Vehicle Technology Demonstrator (RLV-TD), marking a crucial milestone in India's "
            "quest to dramatically reduce space launch costs. The unmanned vehicle was launched from Sriharikota, "
            "reached an altitude of 120 km, and autonomously navigated its return to a precision landing.\n\n"
            "This test brings ISRO one step closer to developing a fully reusable two-stage-to-orbit launch system, "
            "which could reduce launch costs by up to 80%. The RLV-TD successfully demonstrated autonomous guidance, "
            "thermal protection system performance, and landing gear deployment.\n\n"
            "\"This is India's SpaceX moment,\" said ISRO Chairman Dr. S. Somanath. \"We've proven that our "
            "indigenous technology can achieve reusable spaceflight. The next phase will involve a full orbital "
            "mission with satellite deployment and return.\"\n\n"
            "The test also validated ISRO's indigenous carbon-carbon composite thermal protection tiles, which "
            "withstood re-entry temperatures exceeding 2,000°C."
        ),
        "summary": "ISRO's RLV-TD completes orbital return mission, could reduce launch costs by 80%. Indigenous thermal tiles validated.",
        "category_slug": "technology",
        "author": "Arjun Menon",
        "source_name": "ET Science",
        "tags": ["ISRO", "space", "RLV", "reusable-rocket", "Sriharikota"],
        "entities": ["ISRO", "RLV-TD", "S. Somanath", "Sriharikota"],
        "sentiment_score": 0.95,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/586056/pexels-photo-586056.jpeg?w=800",
    },
    {
        "title": "India's Renewable Energy Capacity Surpasses 200 GW Target Ahead of Schedule",
        "content": (
            "India has achieved its 200 GW renewable energy capacity target two years ahead of the 2028 deadline, "
            "according to the Ministry of New and Renewable Energy. Solar power contributes 120 GW, wind energy "
            "65 GW, and other renewables including biomass and small hydro account for the remaining 15 GW.\n\n"
            "The milestone was driven by massive solar installations in Rajasthan, Gujarat, and Tamil Nadu, "
            "combined with a boom in offshore wind projects along India's western coast. Private sector "
            "investment in renewables crossed $40 billion in FY26.\n\n"
            "\"India is now the third-largest renewable energy market globally,\" said Union Minister for "
            "Energy R.K. Singh. \"Our next target is 500 GW by 2030, and we're on track to achieve it.\"\n\n"
            "The achievement is expected to help India meet its Paris Agreement commitments and reduce its "
            "carbon intensity by 45% from 2005 levels."
        ),
        "summary": "India hits 200 GW renewable energy 2 years early. Solar leads with 120 GW. Next target: 500 GW by 2030.",
        "category_slug": "energy",
        "author": "Kavita Reddy",
        "source_name": "ET Energy",
        "tags": ["renewable-energy", "solar", "wind", "climate", "green-energy"],
        "entities": ["Ministry of New and Renewable Energy", "R.K. Singh", "Paris Agreement"],
        "sentiment_score": 0.92,
        "reading_level": "beginner",
        "is_trending": False,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/433308/pexels-photo-433308.jpeg?w=800",
    },
    {
        "title": "Tata Sons Leads $500M Funding Round for Homegrown Semiconductor Startup",
        "content": (
            "Tata Sons has led a $500 million Series C funding round for SignalChip, a Bengaluru-based fabless "
            "semiconductor startup. The investment values the company at $2.8 billion, making it India's most "
            "valuable chip design company. The funding will be used to build a dedicated R&D center in Hyderabad "
            "and expand production partnerships with TSMC and Samsung Foundry.\n\n"
            "SignalChip, founded in 2010, has developed India's first indigenous 4G/5G modem chip and is now "
            "working on a 3nm design for 6G applications. The company holds 180+ patents and employs over "
            "1,200 engineers across India and Israel.\n\n"
            "\"Semiconductor self-reliance is critical for India's digital sovereignty,\" said N. Chandrasekaran, "
            "Chairman of Tata Sons. \"SignalChip represents the best of Indian engineering talent.\"\n\n"
            "The deal comes amid India's aggressive push to become a global semiconductor hub, with the government's "
            "₹76,000 crore India Semiconductor Mission attracting interest from Intel, Micron, and Tower Semiconductor."
        ),
        "summary": "Tata Sons leads $500M round for SignalChip at $2.8B valuation. Building India's semiconductor capability.",
        "category_slug": "startups",
        "author": "Rahul Joshi",
        "source_name": "ET Startups",
        "tags": ["semiconductor", "Tata", "chips", "funding", "5G"],
        "entities": ["Tata Sons", "SignalChip", "N. Chandrasekaran", "TSMC", "Samsung Foundry"],
        "sentiment_score": 0.82,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?w=800",
    },
    {
        "title": "EU Imposes New Digital Services Act Fines on Meta and X for Misinformation",
        "content": (
            "The European Union has imposed a combined €2.3 billion in fines on Meta and X (formerly Twitter) "
            "for failing to adequately address misinformation and hate speech under the Digital Services Act. "
            "Meta was fined €1.5 billion for insufficient moderation of AI-generated deepfakes, while X was "
            "fined €800 million for inadequate transparency reporting.\n\n"
            "European Commissioner for Digital Affairs Henna Virkkunen said the platforms had \"systematically "
            "failed\" to meet their obligations under the DSA, particularly regarding recommender system "
            "transparency and the rapid removal of illegal content.\n\n"
            "Meta's VP of Global Affairs, Nick Clegg, called the fine \"disproportionate\" and announced the "
            "company would appeal. X CEO Linda Yaccarino said the company was \"deeply disappointed\" and "
            "questioned the EU's regulatory overreach.\n\n"
            "The fines represent 6% of each company's annual EU revenue, the maximum penalty under the DSA. "
            "This marks the largest single enforcement action since the law took full effect in February 2024."
        ),
        "summary": "EU fines Meta €1.5B and X €800M under DSA for inadequate misinformation controls. Both to appeal.",
        "category_slug": "world",
        "author": "Siddharth Rao",
        "source_name": "ET World",
        "tags": ["EU", "DSA", "Meta", "X", "regulation", "fines"],
        "entities": ["European Union", "Meta", "X", "Henna Virkkunen", "Nick Clegg", "Linda Yaccarino"],
        "sentiment_score": -0.3,
        "reading_level": "advanced",
        "is_trending": True,
        "is_breaking": True,
        "image_url": "https://images.pexels.com/photos/607812/pexels-photo-607812.jpeg?w=800",
    },
    {
        "title": "India's GDP Growth Accelerates to 7.3% in Q3 FY26, Beats All Estimates",
        "content": (
            "India's gross domestic product grew at 7.3% in the October-December quarter of FY26, significantly "
            "beating market expectations of 6.5% and outpacing China's 4.8% growth in the same period. The data "
            "released by the Ministry of Statistics showed robust performance in manufacturing, services, and "
            "agriculture sectors.\n\n"
            "Manufacturing grew at 8.1%, its fastest pace in nine quarters, driven by strong export demand and "
            "the Make in India initiative's success in attracting electronics and automobile manufacturing. "
            "Agriculture grew at 4.5%, supported by a bountiful monsoon season.\n\n"
            "\"India continues to be the fastest-growing major economy,\" said Chief Economic Adviser V. Anantha "
            "Nageswaran. \"The growth is broad-based, sustainable, and underpinned by strong domestic consumption.\"\n\n"
            "The strong GDP print has led several brokerages, including Goldman Sachs and Morgan Stanley, to "
            "revise their full-year FY26 growth estimates upward to 7.0% from 6.6% earlier."
        ),
        "summary": "India's Q3 FY26 GDP at 7.3% crushes estimates, led by 8.1% manufacturing growth. Fastest-growing major economy.",
        "category_slug": "economy",
        "author": "Meera Subramanian",
        "source_name": "ET Economy",
        "tags": ["GDP", "growth", "economy", "manufacturing", "services"],
        "entities": ["Ministry of Statistics", "V. Anantha Nageswaran", "Goldman Sachs", "Morgan Stanley"],
        "sentiment_score": 0.88,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/7567443/pexels-photo-7567443.jpeg?w=800",
    },
    {
        "title": "OpenAI Launches GPT-5 Turbo with Native Agent Capabilities",
        "content": (
            "OpenAI has released GPT-5 Turbo, its most powerful model yet, featuring native agentic capabilities "
            "that allow the AI to autonomously browse the web, write and execute code, manage files, and interact "
            "with external APIs — all without plugin dependencies.\n\n"
            "The model introduces 'persistent memory' across sessions, a 4-million-token context window, and "
            "a new 'delegation protocol' that allows GPT-5 to spawn sub-agents for parallel task execution. "
            "OpenAI claims the model achieves 95.1% on the SWE-bench Verified benchmark.\n\n"
            "\"We're entering the era of AI that doesn't just answer questions but actually completes work,\" "
            "said Sam Altman, CEO of OpenAI. \"GPT-5 Turbo can handle hours of complex work autonomously.\"\n\n"
            "The launch intensifies the AI race, with Google, Anthropic, and Meta all expected to release "
            "competing agentic models in the coming months. Enterprise pricing starts at $15 per million "
            "input tokens."
        ),
        "summary": "GPT-5 Turbo features 4M token context, native agents, persistent memory. 95.1% SWE-bench score.",
        "category_slug": "ai-ml",
        "author": "Aditi Krishnan",
        "source_name": "ET Tech",
        "tags": ["OpenAI", "GPT-5", "AI-agents", "LLM", "AGI"],
        "entities": ["OpenAI", "GPT-5 Turbo", "Sam Altman", "Google", "Anthropic", "Meta"],
        "sentiment_score": 0.75,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": True,
        "image_url": "https://images.pexels.com/photos/8386434/pexels-photo-8386434.jpeg?w=800",
    },
    {
        "title": "Infosys Wins $2 Billion AI Transformation Deal with Deutsche Bank",
        "content": (
            "Infosys has secured its largest-ever deal, a $2 billion multi-year AI transformation contract with "
            "Deutsche Bank. The engagement covers enterprise-wide AI integration, cloud migration, and the "
            "development of an AI-powered risk management platform using generative AI.\n\n"
            "Under the deal, Infosys will deploy over 5,000 engineers to Deutsche Bank's operations across "
            "Germany, the UK, and India. The project will leverage Infosys's Topaz AI platform and Google Cloud's "
            "Vertex AI infrastructure.\n\n"
            "\"This deal validates India's IT industry's pivot from traditional services to AI-first transformation,\" "
            "said Salil Parekh, CEO of Infosys. \"We're not just implementing technology — we're reimagining "
            "how banking works.\"\n\n"
            "The announcement sent Infosys shares up 4.5% on the BSE, adding ₹28,000 crore to the company's "
            "market capitalization. Analysts see the deal as a bellwether for the Indian IT sector's AI revenue growth."
        ),
        "summary": "Infosys bags $2B deal with Deutsche Bank — largest in company history. AI transformation across banking ops.",
        "category_slug": "technology",
        "author": "Nikhil Kapoor",
        "source_name": "ET Tech",
        "tags": ["Infosys", "Deutsche Bank", "AI-deal", "IT-services", "cloud"],
        "entities": ["Infosys", "Deutsche Bank", "Salil Parekh", "Topaz AI", "Google Cloud"],
        "sentiment_score": 0.85,
        "reading_level": "intermediate",
        "is_trending": True,
        "is_breaking": False,
        "image_url": "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=800",
    },
]


STORY_ARCS = [
    {
        "title": "India's AI Revolution: From Consumer to Creator",
        "slug": "india-ai-revolution",
        "description": "Tracking India's transformation from an AI-consuming nation to a global AI innovation hub, covering policy, startups, talent, and infrastructure.",
        "entities": ["NASSCOM", "IndiaAI Mission", "Krutrim", "Sarvam AI", "Google", "OpenAI"],
        "image_url": "https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?w=800",
    },
    {
        "title": "The Great Rate Pause: RBI's Monetary Policy Tightrope",
        "slug": "rbi-rate-pause",
        "description": "Following the RBI's interest rate decisions and their impact on markets, banking, and the broader economy.",
        "entities": ["RBI", "Sanjay Malhotra", "MPC", "US Federal Reserve"],
        "image_url": "https://images.pexels.com/photos/4386476/pexels-photo-4386476.jpeg?w=800",
    },
    {
        "title": "India's Semiconductor Ambition: Building the Chip Ecosystem",
        "slug": "india-semiconductor-push",
        "description": "India's journey to become a global semiconductor design and manufacturing hub, from policy to execution.",
        "entities": ["Tata Sons", "SignalChip", "India Semiconductor Mission", "TSMC", "Intel", "Micron"],
        "image_url": "https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?w=800",
    },
]


BRIEFINGS = [
    {
        "title": "Morning Market Pulse — March 29, 2026",
        "slug": "morning-market-pulse-mar-29",
        "topic": "Markets & Economy",
        "summary": "A synthesis of today's key market movements, FII flows, and economic indicators.",
        "key_insights": [
            "Sensex rallied 800+ points on record FII inflows of ₹12,500 crore",
            "RBI's accommodative stance signals possible rate cut in next policy meeting",
            "India's GDP at 7.3% makes it the fastest-growing major economy",
            "10-year bond yield fell 8 bps to 6.72% on policy optimism",
        ],
        "qa_pairs": [
            {"q": "Why are FIIs investing heavily in India?", "a": "Attractive valuations, weakening dollar, and India's strong 7.3% GDP growth trajectory."},
            {"q": "Will RBI cut rates next meeting?", "a": "The shift to accommodative stance signals readiness, but it depends on inflation staying below 4.5%."},
            {"q": "Which sectors are leading the rally?", "a": "Banking (HDFC Bank +3.2%) and IT (Infosys +2.8%) are leading, supported by strong deal wins."},
        ],
        "image_url": "https://images.pexels.com/photos/6801648/pexels-photo-6801648.jpeg?w=800",
    },
    {
        "title": "AI Arms Race: What Gemini 3.0 and GPT-5 Mean for Enterprise",
        "slug": "ai-arms-race-gemini-gpt5",
        "topic": "Technology & AI",
        "summary": "Breaking down the implications of Google and OpenAI's latest model releases for businesses.",
        "key_insights": [
            "Gemini 3.0 Ultra: 2M token context, reasoning traces, $0.00375/1K tokens",
            "GPT-5 Turbo: 4M token context, native agents, persistent memory",
            "Both models target enterprise workflows — coding, analysis, planning",
            "Indian IT firms like Infosys are already integrating these models into client solutions",
        ],
        "qa_pairs": [
            {"q": "Which model is better for enterprise?", "a": "GPT-5 Turbo for autonomous agents, Gemini 3.0 Ultra for multimodal reasoning and cost efficiency."},
            {"q": "How does this affect Indian IT companies?", "a": "Positively — Infosys's $2B Deutsche Bank deal is built on AI transformation using these models."},
        ],
        "image_url": "https://images.pexels.com/photos/17483868/pexels-photo-17483868.jpeg?w=800",
    },
]


class Command(BaseCommand):
    help = "Seed demo data: categories, articles, story arcs, briefings, users."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("[SEED] Seeding demo data..."))
        self._seed_categories()
        self._seed_articles()
        self._seed_story_arcs()
        self._seed_briefings()
        self._seed_users()
        self.stdout.write(self.style.SUCCESS("[OK] Seeding complete!"))

    def _seed_categories(self):
        from apps.news.models import Category
        for cat_data in CATEGORIES:
            Category.objects.update_or_create(
                slug=cat_data["slug"],
                defaults=cat_data,
            )
        self.stdout.write(f"  [+] {len(CATEGORIES)} categories seeded")

    def _seed_articles(self):
        from apps.news.models import Article, Category
        from django.utils.text import slugify
        import uuid

        for i, art in enumerate(ARTICLES):
            category = Category.objects.filter(slug=art["category_slug"]).first()
            slug = slugify(art["title"])[:500]
            pub_date = timezone.now() - timedelta(hours=random.randint(1, 72))

            Article.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": art["title"],
                    "content": art["content"],
                    "summary": art["summary"],
                    "source_url": f"https://economictimes.com/article/{slug}",
                    "source_name": art["source_name"],
                    "author": art["author"],
                    "image_url": art["image_url"],
                    "category": category,
                    "tags": art["tags"],
                    "entities": art["entities"],
                    "sentiment_score": art["sentiment_score"],
                    "reading_level": art["reading_level"],
                    "reading_time_minutes": random.randint(3, 12),
                    "views_count": random.randint(500, 50000),
                    "likes_count": random.randint(20, 2000),
                    "is_trending": art["is_trending"],
                    "is_breaking": art["is_breaking"],
                    "published_at": pub_date,
                    "is_processed": True,
                },
            )
        self.stdout.write(f"  [+] {len(ARTICLES)} articles seeded")

    def _seed_story_arcs(self):
        from apps.story_arc.models import StoryArc, TimelineEvent
        from apps.news.models import Article

        for arc_data in STORY_ARCS:
            arc, _ = StoryArc.objects.update_or_create(
                slug=arc_data["slug"],
                defaults={
                    "title": arc_data["title"],
                    "description": arc_data["description"],
                    "entities": arc_data["entities"],
                    "image_url": arc_data.get("image_url", ""),
                },
            )

            # Link relevant articles (SQLite doesn't support __contains on JSON)
            all_articles = Article.objects.all()
            for article in all_articles:
                if isinstance(article.entities, list):
                    for entity in arc_data["entities"][:3]:
                        if entity in article.entities:
                            arc.articles.add(article)
                            break

            # Create timeline events
            if not arc.events.exists():
                for j in range(3):
                    TimelineEvent.objects.create(
                        story_arc=arc,
                        title=f"Key development #{j+1} in {arc.title[:50]}",
                        description=f"A significant milestone in this ongoing story.",
                        event_date=timezone.now() - timedelta(days=random.randint(1, 90)),
                        sentiment=random.uniform(-0.3, 0.9),
                        importance=random.randint(5, 10),
                    )

        self.stdout.write(f"  [+] {len(STORY_ARCS)} story arcs seeded")

    def _seed_briefings(self):
        from apps.navigator.models import Briefing
        from apps.news.models import Article

        for brief_data in BRIEFINGS:
            briefing, _ = Briefing.objects.update_or_create(
                slug=brief_data["slug"],
                defaults={
                    "title": brief_data["title"],
                    "topic": brief_data["topic"],
                    "summary": brief_data["summary"],
                    "key_insights": brief_data["key_insights"],
                    "qa_pairs": brief_data["qa_pairs"],
                    "image_url": brief_data.get("image_url", ""),
                },
            )
            # Link some articles
            articles = Article.objects.order_by("?")[:4]
            briefing.source_articles.add(*articles)

        self.stdout.write(f"  [+] {len(BRIEFINGS)} briefings seeded")

    def _seed_users(self):
        # Create demo users
        demo_users = [
            {
                "username": "demo_investor",
                "email": "investor@demo.com",
                "password": "demo1234",
                "profile_type": "investor",
                "interests": ["markets", "stocks", "mutual-funds", "IPO"],
                "financial_goals": ["wealth-growth", "retirement"],
            },
            {
                "username": "demo_founder",
                "email": "founder@demo.com",
                "password": "demo1234",
                "profile_type": "founder",
                "interests": ["startups", "funding", "AI", "fintech"],
                "financial_goals": ["fundraising", "scale-up"],
            },
            {
                "username": "demo_student",
                "email": "student@demo.com",
                "password": "demo1234",
                "profile_type": "student",
                "interests": ["technology", "AI", "career", "economy"],
                "financial_goals": ["career-start", "savings"],
            },
        ]

        for u in demo_users:
            user, created = User.objects.get_or_create(
                username=u["username"],
                defaults={
                    "email": u["email"],
                    "profile_type": u["profile_type"],
                    "interests": u["interests"],
                    "financial_goals": u["financial_goals"],
                    "onboarding_completed": True,
                },
            )
            if created:
                user.set_password(u["password"])
                user.save()

        self.stdout.write(f"  [+] {len(demo_users)} demo users seeded")
