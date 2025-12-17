from app.models import Prediction
from app import db
import random


class PredictionsManager:
    """Manager for handling predictions"""

    # Prediction categories
    CATEGORIES = {
        'luck': '🍀 Luck',
        'love': '❤️ Love',
        'career': '💼 Career',
        'wisdom': '📚 Wisdom',
        'friendship': '👥 Friendship',
        'travel': '✈️ Travel',
        'health': '💪 Health',
        'creativity': '🎨 Creativity',
        'funny': '😄 Funny',
        'inspiration': '🌟 Inspirational'
    }

    @staticmethod
    def initialize_default_predictions():
        """Initialize default predictions"""
        try:
            # Check if predictions already exist
            if Prediction.query.first() is not None:
                print("✅ Predictions already initialized")
                return

            default_predictions = [
                # Luck (30 predictions)
                ('luck', 'Unexpected luck awaits you.'),
                ('luck', 'A brilliant idea will strike you soon.'),
                ('luck', 'Luck will smile on you on Thursday.'),
                ('luck', 'Courage opens golden doors.'),
                ('luck', 'A financial surprise is coming your way.'),
                ('luck', 'Your persistence will soon pay off.'),
                ('luck', 'Get ready for a pleasant surprise.'),
                ('luck', 'Luck is on your side.'),
                ('luck', 'Success awaits you in a new endeavor.'),
                ('luck', 'Fate has prepared a gift for you.'),
                ('luck', 'Everything you seek will be found.'),
                ('luck', 'A big breakthrough awaits you soon.'),
                ('luck', 'Fortune has turned to face you.'),
                ('luck', 'Your star is rising.'),
                ('luck', 'A streak of good luck is ahead.'),
                ('luck', 'You are on the right path.'),
                ('luck', 'Take a risk – you will be rewarded.'),
                ('luck', 'Luck will come from an unexpected place.'),
                ('luck', 'You will soon get what you have long dreamed of.'),
                ('luck', 'Belief in yourself leads to victory.'),
                ('luck', 'A win awaits you (not necessarily monetary).'),
                ('luck', 'Your ship will soon arrive in harbor.'),
                ('luck', 'The wind of luck will fill your sails.'),
                ('luck', 'Triumph awaits you.'),
                ('luck', 'Luck favors the bold.'),
                ('luck', 'The time to reap rewards is near.'),
                ('luck', 'The stars favor you.'),
                ('luck', 'Dizzying success awaits you.'),
                ('luck', 'A lucky chance will change everything.'),
                ('luck', 'Golden opportunities lie ahead.'),

                # Love (30 predictions)
                ('love', 'A new romantic acquaintance awaits you.'),
                ('love', 'Important words will be spoken soon.'),
                ('love', 'Your heart knows the answer.'),
                ('love', 'Love is waiting for you around the corner.'),
                ('love', 'An old feeling may reignite.'),
                ('love', 'You are valued more than you think.'),
                ('love', 'Soon a person will enter your life who changes everything.'),
                ('love', 'Speak about your feelings – you will be heard.'),
                ('love', 'A life-changing meeting is near.'),
                ('love', 'Your attractiveness is at its peak.'),
                ('love', 'Someone secretly admires you.'),
                ('love', 'A romantic adventure awaits you.'),
                ('love', 'Trust your heart.'),
                ('love', 'Harmony will return to your relationship.'),
                ('love', 'You will soon hear a confession.'),
                ('love', 'Love is a journey, not a destination.'),
                ('love', 'New relationships will start unexpectedly.'),
                ('love', 'You will meet a kindred spirit.'),
                ('love', 'Show tenderness – you will receive double in return.'),
                ('love', 'A memorable date awaits you.'),
                ('love', 'Your sincerity will capture someone\'s heart.'),
                ('love', 'Listen not only with your ears but with your heart.'),
                ('love', 'A big surprise from your loved one awaits you.'),
                ('love', 'A moment of complete understanding is near.'),
                ('love', 'Love is the answer.'),
                ('love', 'People are drawn to you.'),
                ('love', 'Your significant other is thinking about you right now.'),
                ('love', 'Don\'t be afraid to be vulnerable.'),
                ('love', 'Romance will paint your life with new colors.'),
                ('love', 'Your charm is irresistible.'),

                # Career (30 predictions)
                ('career', 'A promotion or interesting offer awaits you.'),
                ('career', 'A bold idea will lead to success.'),
                ('career', 'Your work will soon be appreciated.'),
                ('career', 'Investments (not only financial) will pay off.'),
                ('career', 'Business partnership will be fruitful.'),
                ('career', 'A new promising path will open soon.'),
                ('career', 'Colleagues will support you.'),
                ('career', 'You will be noticed and highly valued.'),
                ('career', 'Boldly ask for what you are worth.'),
                ('career', 'A profitable deal or contract awaits you.'),
                ('career', 'Management will be pleased with your work.'),
                ('career', 'Don\'t be afraid to change direction.'),
                ('career', 'You will soon receive a well-deserved reward.'),
                ('career', 'The new project will become your star.'),
                ('career', 'Financial well-being is on its way.'),
                ('career', 'Your skills are in high demand.'),
                ('career', 'A business trip will bring benefits.'),
                ('career', 'An important career decision awaits you.'),
                ('career', 'Success will come through cooperation.'),
                ('career', 'Trust your professional intuition.'),
                ('career', 'Positive changes at work await you.'),
                ('career', 'Money will come from an unexpected source.'),
                ('career', 'Your reputation is your greatest asset.'),
                ('career', 'You will soon celebrate a professional victory.'),
                ('career', 'Don\'t miss the chance to take initiative.'),
                ('career', 'A period of growth and development awaits you.'),
                ('career', 'Difficulties will lead to new opportunities.'),
                ('career', 'Your time is money – spend it wisely.'),
                ('career', 'An interesting business trip awaits you.'),
                ('career', 'Networking will pay dividends.'),

                # Wisdom (30 predictions)
                ('wisdom', 'Silence is your best advisor today.'),
                ('wisdom', 'The answer will come when you stop searching for it.'),
                ('wisdom', 'Trust your inner voice.'),
                ('wisdom', 'Sometimes you need to get lost to find yourself.'),
                ('wisdom', 'Calmness is your superpower.'),
                ('wisdom', 'The most important lesson is to be kind to yourself.'),
                ('wisdom', 'Time heals, but wisdom prevents wounds.'),
                ('wisdom', 'Your intuition never deceives you.'),
                ('wisdom', 'Happiness is a journey, not a destination.'),
                ('wisdom', 'Listen to the whisper of your heart.'),
                ('wisdom', 'The past is a lesson, the future is an opportunity.'),
                ('wisdom', 'Sometimes you just need to let go.'),
                ('wisdom', 'Your soul craves creativity.'),
                ('wisdom', 'Pause. The universe is whispering to you.'),
                ('wisdom', 'Wisdom comes with the ability to wonder.'),
                ('wisdom', 'The longest journey begins with a single step.'),
                ('wisdom', 'You are stronger than you think.'),
                ('wisdom', 'Allow yourself to be happy here and now.'),
                ('wisdom', 'Your life is a book. Don\'t be afraid to start a new chapter.'),
                ('wisdom', 'All the light you need is within you.'),
                ('wisdom', 'Trust the flow of life.'),
                ('wisdom', 'Sometimes "no" is the wisest answer.'),
                ('wisdom', 'Your calmness is the key to success.'),
                ('wisdom', 'Enjoy the simple moments.'),
                ('wisdom', 'Everything you need is already inside.'),
                ('wisdom', 'Look inside yourself – the answer is there.'),
                ('wisdom', 'The world inside you reflects the world around you.'),
                ('wisdom', 'Patience turns dreams into reality.'),
                ('wisdom', 'Today is a gift. That\'s why it\'s called the present.'),
                ('wisdom', 'Your inner harmony is the key to everything.'),

                # Friendship (30 predictions)
                ('friendship', 'An old friend will soon get in touch.'),
                ('friendship', 'An interesting acquaintance awaits you.'),
                ('friendship', 'You will help a friend, and it will come back to you.'),
                ('friendship', 'Your charm attracts people.'),
                ('friendship', 'You will soon be invited to a fun party.'),
                ('friendship', 'A sincere conversation will strengthen friendship.'),
                ('friendship', 'You will find common ground with someone you argued with.'),
                ('friendship', 'A friend needs your support.'),
                ('friendship', 'New friends will appear in an unexpected place.'),
                ('friendship', 'Your sense of humor will win everyone over.'),
                ('friendship', 'Don\'t be afraid to make the first call.'),
                ('friendship', 'An unforgettable meeting awaits you.'),
                ('friendship', 'You are the life of the party, even if you don\'t notice it.'),
                ('friendship', 'Trust is the best foundation for relationships.'),
                ('friendship', 'You will soon make a useful acquaintance.'),
                ('friendship', 'Your advice is very important to someone.'),
                ('friendship', 'Pleasant guests await you.'),
                ('friendship', 'Communication will open new horizons.'),
                ('friendship', 'A friend will tell you what you have long wanted to hear.'),
                ('friendship', 'Your generosity will be duly appreciated.'),
                ('friendship', 'You are surrounded by people who love you.'),
                ('friendship', 'Share your ideas boldly.'),
                ('friendship', 'A meeting with an interesting person awaits you.'),
                ('friendship', 'The joy you share multiplies.'),
                ('friendship', 'You will soon receive an unexpected invitation.'),
                ('friendship', 'Your sincerity attracts good people.'),
                ('friendship', 'Don\'t be afraid to be open.'),
                ('friendship', 'Warm meetings await you.'),
                ('friendship', 'The friendship you value will become even stronger.'),
                ('friendship', 'Your kind word will change someone\'s day.'),

                # Travel (30 predictions)
                ('travel', 'A trip awaits you soon.'),
                ('travel', 'Step out of your comfort zone – it\'s interesting out there.'),
                ('travel', 'A pleasant surprise from fate awaits you.'),
                ('travel', 'A new hobby will captivate you.'),
                ('travel', 'Don\'t be afraid to change plans.'),
                ('travel', 'A trip to the water awaits you.'),
                ('travel', 'Everything will soon change for the better.'),
                ('travel', 'Try what you have long been afraid of.'),
                ('travel', 'A ticket to a new life awaits you.'),
                ('travel', 'Adventure begins where maps end.'),
                ('travel', 'Life has prepared a surprise for you.'),
                ('travel', 'Pack your bags.'),
                ('travel', 'Positive changes are on the way.'),
                ('travel', 'You will discover a new place.'),
                ('travel', 'Fate will bring you together with an interesting person.'),
                ('travel', 'A road full of discoveries awaits you.'),
                ('travel', 'Don\'t cling to the old – the new is better.'),
                ('travel', 'You will soon change your scenery.'),
                ('travel', 'Your life will shine with new colors.'),
                ('travel', 'Take a risk – and you won\'t regret it.'),
                ('travel', 'An event awaits you that will broaden your horizons.'),
                ('travel', 'New experiences are on the way.'),
                ('travel', 'You will embark on a journey that will change you.'),
                ('travel', 'You will soon break out of your usual boundaries.'),
                ('travel', 'Get ready for vivid impressions.'),
                ('travel', 'The universe is leading you to new horizons.'),
                ('travel', 'Don\'t miss the chance for change.'),
                ('travel', 'A discovery (big or small) awaits you.'),
                ('travel', 'It\'s time for a new beginning.'),
                ('travel', 'Trust the flow of life.'),

                # Health (30 predictions)
                ('health', 'Take care of yourself – you deserve it.'),
                ('health', 'You will soon find the perfect balance.'),
                ('health', 'Your energy will increase.'),
                ('health', 'A small habit will change a lot.'),
                ('health', 'Listen to your body.'),
                ('health', 'You will find inner peace.'),
                ('health', 'A walk in nature will bring clarity.'),
                ('health', 'Health is your greatest wealth.'),
                ('health', 'A new sporting experience will please you.'),
                ('health', 'You will find what gives you strength.'),
                ('health', 'Rest is not a luxury, but a necessity.'),
                ('health', 'Your body will thank you.'),
                ('health', 'Inner peace begins with small steps.'),
                ('health', 'You are on the path to the best version of yourself.'),
                ('health', 'Harmony within attracts harmony without.'),
                ('health', 'Allow yourself to relax without guilt.'),
                ('health', 'You will soon feel a surge of energy.'),
                ('health', 'Self-care is the best investment.'),
                ('health', 'Find your own rhythm.'),
                ('health', 'Peace of mind is your fortress.'),
                ('health', 'Silence and peace will restore your strength.'),
                ('health', 'Attention to yourself is the key to harmony.'),
                ('health', 'Your health is the foundation of success.'),
                ('health', 'Don\'t forget to breathe deeply.'),
                ('health', 'Know when to stop and rest.'),
                ('health', 'Good sleep is the best medicine.'),
                ('health', 'Enjoy movement and activity.'),
                ('health', 'Your body deserves care and attention.'),
                ('health', 'Listen to your body\'s signals.'),
                ('health', 'A healthy mind in a healthy body.'),

                # Creativity (30 predictions)
                ('creativity', 'The muse will visit you.'),
                ('creativity', 'Your creativity will inspire many.'),
                ('creativity', 'Share your talent boldly.'),
                ('creativity', 'The idea you are nurturing is beautiful.'),
                ('creativity', 'A creative breakthrough awaits you.'),
                ('creativity', 'Don\'t be afraid to create for the soul.'),
                ('creativity', 'Your imagination is a source of wonders.'),
                ('creativity', 'You will soon create something amazing.'),
                ('creativity', 'Inspiration will come from childhood memories.'),
                ('creativity', 'Create as you feel.'),
                ('creativity', 'Your project awaits success.'),
                ('creativity', 'Allow yourself to be impractical.'),
                ('creativity', 'You will find beauty in the ordinary.'),
                ('creativity', 'Your creativity will be appreciated.'),
                ('creativity', 'Dream bigger.'),
                ('creativity', 'Art will save your day.'),
                ('creativity', 'Don\'t judge, just create.'),
                ('creativity', 'Insight awaits you.'),
                ('creativity', 'You will discover a new talent.'),
                ('creativity', 'Your creativity is needed by the world.'),
                ('creativity', 'Allow yourself to be bold in creativity.'),
                ('creativity', 'Your ideas will change the world for the better.'),
                ('creativity', 'Creativity is freedom of expression.'),
                ('creativity', 'Don\'t be afraid to experiment.'),
                ('creativity', 'Your unique perspective is your advantage.'),
                ('creativity', 'An artist lives in each of us.'),
                ('creativity', 'Give free rein to your imagination.'),
                ('creativity', 'Creativity heals the soul.'),
                ('creativity', 'Your talent will be noticed.'),
                ('creativity', 'Create what the world is missing.'),

                # Funny (30 predictions)
                ('funny', 'Be careful with bananas this week.'),
                ('funny', 'You will soon find your lost sock.'),
                ('funny', 'Your toast tomorrow will be the most memorable.'),
                ('funny', 'An awkward but funny compliment awaits you.'),
                ('funny', 'Coffee will be especially tasty on Wednesday.'),
                ('funny', 'You will accidentally become a meme hero.'),
                ('funny', 'Someone thinks you are a wizard. Don\'t disappoint them.'),
                ('funny', 'You will soon sing in the shower especially inspirationally.'),
                ('funny', 'Your next selfie will become iconic.'),
                ('funny', 'The bus will arrive on time. Amazing but true.'),
                ('funny', 'You will meet someone in a funny hat, and it will matter.'),
                ('funny', 'The soup will be perfectly salted.'),
                ('funny', 'You will remember where you put your keys.'),
                ('funny', 'The cat will deign to let you pet it.'),
                ('funny', 'The dumplings in the package will be whole.'),
                ('funny', 'You will find money in an old jacket.'),
                ('funny', 'WiFi will work on its own.'),
                ('funny', 'You will guess the password on the first try.'),
                ('funny', 'Rain will start exactly when you are already home.'),
                ('funny', 'You will become an accidental expert in something very strange.'),
                ('funny', 'A bird will look at you with deep understanding.'),
                ('funny', 'Your turn in the store will be the fastest.'),
                ('funny', 'You will finally understand the IKEA instructions.'),
                ('funny', 'The traffic light will turn green as if by magic.'),
                ('funny', 'You will answer the call just before it stops ringing.'),
                ('funny', 'The popcorn in the microwave won\'t burn.'),
                ('funny', 'You will sneeze exactly three times, no more, no less.'),
                ('funny', 'Your toast will fall butter side up. Believe in miracles.'),
                ('funny', 'You will meet your grandmother\'s double.'),
                ('funny', 'The weather on the weekend will be exactly as you wanted.'),

                # Inspirational (30 predictions)
                ('inspiration', 'Tomorrow will be better than yesterday.'),
                ('inspiration', 'Every day is a blank slate.'),
                ('inspiration', 'Your smile changes the world.'),
                ('inspiration', 'The good you do comes back to you.'),
                ('inspiration', 'You are the author of your life.'),
                ('inspiration', 'Hope is the most reliable compass.'),
                ('inspiration', 'Small steps lead to big goals.'),
                ('inspiration', 'Light always conquers darkness.'),
                ('inspiration', 'Your presence is a gift to others.'),
                ('inspiration', 'Time is the most valuable resource.'),
                ('inspiration', 'Truth is simple, but we like to complicate it.'),
                ('inspiration', 'Life is 10% what happens and 90% how you react to it.'),
                ('inspiration', 'Sometimes you need to slow down to speed up.'),
                ('inspiration', 'You are unique, and that is your strength.'),
                ('inspiration', 'The sun always shines behind the clouds.'),
                ('inspiration', 'The shortest path is an honest one.'),
                ('inspiration', 'Doubts are just clouds on the sky of your confidence.'),
                ('inspiration', 'The secret of happiness is gratitude.'),
                ('inspiration', 'You are not a tree; you can change your position.'),
                ('inspiration', 'The future is created today.'),
                ('inspiration', 'Your thoughts shape your reality.'),
                ('inspiration', 'Act as if everything is possible.'),
                ('inspiration', 'Sometimes just being is enough.'),
                ('inspiration', 'You are closer to your dream than it seems.'),
                ('inspiration', 'A problem is a disguised opportunity.'),
                ('inspiration', 'Your breath is the rhythm of the universe within you.'),
                ('inspiration', 'Trust the magic of new beginnings.'),
                ('inspiration', 'You are not alone on your path.'),
                ('inspiration', 'Everything you need will come at the right time.')
            ]

            # Add predictions to database
            for category, text in default_predictions:
                prediction = Prediction(
                    category=category,
                    text=text
                )
                db.session.add(prediction)

            db.session.commit()
            print(f"✅ Initialized {len(default_predictions)} predictions")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error initializing predictions: {e}")
            raise

    @staticmethod
    def get_random_prediction(category=None):
        """Get a random prediction"""
        try:
            query = Prediction.query

            # Filter by category if specified
            if category and category in PredictionsManager.CATEGORIES:
                query = query.filter_by(category=category)

            # Get all predictions
            all_predictions = query.all()

            if not all_predictions:
                return None, "No predictions for today 😊"

            # Select random prediction
            random_prediction = random.choice(all_predictions)

            # Get category name
            category_name = PredictionsManager.CATEGORIES.get(
                random_prediction.category,
                random_prediction.category
            )

            return random_prediction, category_name

        except Exception as e:
            print(f"❌ Error getting prediction: {e}")
            return None, "An error occurred while getting prediction"

    @staticmethod
    def get_all_categories():
        """Get all prediction categories"""
        return PredictionsManager.CATEGORIES

    @staticmethod
    def get_predictions_count():
        """Get number of predictions in database"""
        return Prediction.query.count()