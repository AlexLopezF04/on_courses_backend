from .usuario import UserSerializer, UserWriteSerializer, RegisterSerializer
from .categoria import CategorySerializer
from .modulo import ModuleSerializer
from .leccion import LessonSerializer, LessonDetailSerializer
from .recurso import ResourceSerializer
from .curso import CourseListSerializer, CourseDetailSerializer, CourseWriteSerializer
from .foro import (
    ForumPostSerializer,
    ForumThreadSerializer,
    ForumThreadDetailSerializer,
    ForumThreadWriteSerializer,
    ForumPostWriteSerializer,
)
from .anuncio import AnnouncementSerializer, AnnouncementWriteSerializer
from .comentario_leccion import LessonCommentSerializer, LessonCommentWriteSerializer
from .inscripcion import EnrollmentSerializer, EnrollmentWriteSerializer
from .progreso_leccion import LessonProgressSerializer, LessonProgressWriteSerializer
from .pregunta import QuestionBankSerializer, QuestionBankWriteSerializer
from .examen import ExamSerializer, ExamDetailSerializer, ExamWriteSerializer, ExamQuestionSerializer
from .intento import ExamAttemptSerializer, ExamAttemptWriteSerializer
from .certificado import CertificateSerializer
from .logro import AchievementSerializer, UserAchievementSerializer
from .resena import ReviewSerializer, ReviewWriteSerializer
from .carrito import CartSerializer, CartItemSerializer, CartItemWriteSerializer
from .cupon import CouponSerializer
from .orden import OrderSerializer, OrderWriteSerializer
from .soporte import SupportTicketSerializer, SupportTicketWriteSerializer
