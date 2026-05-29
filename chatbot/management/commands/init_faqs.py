from django.core.management.base import BaseCommand
from chatbot.models import ChatFAQ


class Command(BaseCommand):
    help = 'Initialize sample FAQs for the chatbot'

    def handle(self, *args, **options):
        faqs_data = [
            {
                'question': 'How do I track my order?',
                'answer': 'You can track your order in the "My Orders" section. Click on any order to see the current status, estimated delivery time, and order details.',
                'category': 'orders'
            },
            {
                'question': 'What payment methods do you accept?',
                'answer': 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and digital wallets like Apple Pay and Google Pay.',
                'category': 'billing'
            },
            {
                'question': 'Can I modify my order?',
                'answer': 'You can modify orders before they\'re confirmed by the restaurant. Once confirmed, please contact customer support to make changes.',
                'category': 'orders'
            },
            {
                'question': 'What is your refund policy?',
                'answer': 'We offer full refunds for cancelled orders. If your order has already been prepared, a partial refund may apply depending on circumstances.',
                'category': 'billing'
            },
            {
                'question': 'How do I report a technical issue?',
                'answer': 'You can report technical issues directly through this chat or email support@restaurant-system.com with details about the problem and screenshots if possible.',
                'category': 'technical'
            },
            {
                'question': 'Is the app available on mobile?',
                'answer': 'Yes! Our app is available on both iOS and Android. Search for our restaurant app in your device\'s app store.',
                'category': 'technical'
            },
            {
                'question': 'What are your operating hours?',
                'answer': 'Our kitchen is open Monday-Sunday, 10:00 AM - 11:00 PM. Orders placed after 10:30 PM may be prepared for next-day delivery.',
                'category': 'restaurant'
            },
            {
                'question': 'Do you deliver to my area?',
                'answer': 'Enter your address in our app to see if delivery is available in your area. We currently deliver within a 5-mile radius of our main location.',
                'category': 'orders'
            },
            {
                'question': 'Is there a delivery fee?',
                'answer': 'Delivery fees vary by distance. You\'ll see the exact fee before confirming your order. Free delivery is available for orders over $30.',
                'category': 'billing'
            },
            {
                'question': 'Can I customize my order?',
                'answer': 'Absolutely! Most items allow customization. You can add/remove ingredients, choose portions, and specify dietary preferences during checkout.',
                'category': 'orders'
            },
        ]

        created_count = 0
        for faq_data in faqs_data:
            faq, created = ChatFAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'category': faq_data['category'],
                    'active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created FAQ: {faq_data["question"][:50]}...'))

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count} new FAQs!')
        )
