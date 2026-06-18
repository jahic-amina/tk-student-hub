from email.policy import default
import pytest
from datetime import date, timedelta
from requests import session
from sqlmodel import Session, select
from fastapi.testclient import TestClient
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.models.application import ApplicationStatus, Application
from app.models.ad import Ad, AdStatus, AdType
from app.models.notification import Notification, NotificationType
from app.tests.conftest import active_ad




# ============================================================
# GET /applications/ — Admin only
# ============================================================

class TestGetApplicationsAdmin:

    def test_admin_can_get_all_applications(
        self, client: TestClient, session: Session, admin_token: str, 
        student_user, active_ad
    ):
        """Admin can retrieve all applications."""
    
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
            status=ApplicationStatus.pending,
            is_archived=False
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.get(
            "/applications/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["user_id"] == student_user.id

    def test_student_cannot_get_all_applications(
        self, client: TestClient, student_token: str
    ):
        """Non-admin users cannot access the admin list."""
        response = client.get(
            "/applications/",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 403
        assert "You do not have access to this resource." in response.json()["detail"]

    def test_admin_filter_applications_by_status(
        self, client: TestClient, session: Session, admin_token: str,
        student_user, active_ad
    ):
        """Admin can filter applications by status."""
        
        session.refresh(student_user)
        session.refresh(active_ad)

        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
            status=ApplicationStatus.pending,
            is_archived=False
        )
        session.add(app)
        session.flush() 

        response = client.get(
            f"/applications/?app_status={ApplicationStatus.pending.value}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        for item in data:
            assert item["status"] == ApplicationStatus.pending.value

    def test_admin_filter_applications_by_ad_id(
        self, client: TestClient, session: Session, admin_token: str,
        student_user, active_ad, pending_ad, company_user
    ):
        """Admin can filter applications by ad_id."""
        
        app1 = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
            is_archived=False
        )
        app2 = Application(
            user_id=student_user.id,
            ad_id=pending_ad.id,
            cv_path="/uploads/cvs/test2.pdf",
            motivational_letter_path="/uploads/letters/test2.pdf",
            phone="+38761234567",
            is_archived=False
        )
        session.add(app1)
        session.add(app2)
        session.flush()

        response = client.get(
            f"/applications/?ad_id={active_ad.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["ad_id"] == active_ad.id


# ============================================================
# GET /applications/company/all — Company only
# ============================================================

class TestGetCompanyApplications:

    def test_company_can_get_all_their_applications(
        self, client: TestClient, session: Session, company_token: str,
        company_user, student_user, active_ad
    ):
        """Company can retrieve all applications for their ads."""
        from app.models.application import Application
        session.refresh(student_user)
        session.refresh(active_ad)

        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()

        response = client.get(
            "/applications/company/all",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["ad_id"] == active_ad.id

    def test_student_cannot_access_company_applications(
        self, client: TestClient, student_token: str
    ):
        """Students cannot access company-only endpoints."""
        response = client.get(
            "/applications/company/all",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code in [401, 403]

    def test_company_filter_by_status(
        self, client: TestClient, session: Session, company_token: str,
        company_user, student_user, active_ad
    ):
        """Company can filter their applications by status."""
        
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
            status=ApplicationStatus.accepted,
        )
        session.add(app)
        session.flush()

        response = client.get(
            f"/applications/company/all?app_status={ApplicationStatus.accepted.value}",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        for item in data:
            assert item["status"] == ApplicationStatus.accepted.value


# ============================================================
# GET /applications/company/by-ad/{ad_id} — Company only, pagination
# ============================================================

class TestGetCompanyApplicationsByAd:

    def test_company_can_get_applications_for_their_ad(
        self, client: TestClient, session: Session, company_token: str,
        company_user, student_user, active_ad
    ):
        """Company can retrieve applications for a specific ad they own."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
            status=ApplicationStatus.pending
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.get(
            f"/applications/company/by-ad/{active_ad.id}",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["ad_id"] == active_ad.id

    def test_company_cannot_access_other_company_ad(
        self, client: TestClient, session: Session, company_token: str,
        student_user, other_company_ad
    ):
        """Company cannot access applications for ads they don't own."""
        response = client.get(
            f"/applications/company/by-ad/{other_company_ad.id}",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 403
        assert "You do not have access to applications for this ad." in response.json()["detail"]

    def test_ad_not_found_returns_404(
        self, client: TestClient, company_token: str
    ):
        """Non-existent ad returns 404."""
        response = client.get(
            "/applications/company/by-ad/99999",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 404

    def test_pagination_limit_and_offset(
        self, client: TestClient, session: Session, company_token: str,
        company_user, student_user, active_ad
    ):
        """Pagination works with limit and offset."""
        existing_apps = session.exec(select(Application).where(Application.ad_id == active_ad.id)).all()
        for app in existing_apps:
            session.delete(app)
        session.flush()
       
        for i in range(5):
            other_student = User(
                email=f"student_a{i}@test.ba",
                full_name=f"Student {i}",
                password_hash=hash_password("hashed"),
                role=UserRole.member,
                is_active=True,
            )
            session.add(other_student)
            session.flush()
            
            app_obj = Application(
                user_id=other_student.id,
                ad_id=active_ad.id,
                cv_path=f"/uploads/cvs/test{i}.pdf",
                motivational_letter_path=f"/uploads/letters/test{i}.pdf",
                phone="+38761234567",
                is_archived=False,
            )
            session.add(app_obj)
        session.flush()

        response = client.get(
            f"/applications/company/by-ad/{active_ad.id}?limit=2&offset=0",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


# ============================================================
# POST /applications/ — Create application
# ============================================================

class TestCreateApplication:

    def test_student_can_create_application_on_active_ad(
        self, client: TestClient, session: Session, student_token: str,
        student_user, active_ad
    ):
        session.refresh(student_user)
        session.refresh(active_ad)
        
        """Student can apply to an active ad."""
        payload = {
            "ad_id": active_ad.id,
            "cv_path": "/uploads/cvs/student_cv.pdf",
            "motivational_letter_path": "/uploads/letters/motivation.pdf",
            "linkedin_url": "https://www.linkedin.com/in/student-test",
            "phone": "+38761234567",
        }
        response = client.post(
            "/applications/",
            json=payload,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == student_user.id
        assert data["ad_id"] == active_ad.id
        assert data["status"] == "pending"

    def test_cannot_apply_to_non_active_ad(
        self, client: TestClient, student_token: str, pending_ad
    ):
        """Cannot apply to ads that are not active."""
        payload = {
            "ad_id": pending_ad.id,
            "cv_path": "/uploads/cvs/student_cv.pdf",
            "motivational_letter_path": "/uploads/letters/motivation.pdf",
            "phone": "+38761234567",
        }
        response = client.post(
            "/applications/",
            json=payload,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 400
        assert "Ad is not active" in response.json()["detail"]

    def test_cannot_apply_to_expired_ad(
        self, client: TestClient, student_token: str, expired_ad
    ):
        """Cannot apply to expired ads."""
        payload = {
            "ad_id": expired_ad.id,
            "cv_path": "/uploads/cvs/student_cv.pdf",
            "motivational_letter_path": "/uploads/letters/motivation.pdf",
            "phone": "+38761234567",
        }
        response = client.post(
            "/applications/",
            json=payload,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 400

    def test_cannot_duplicate_application(
        self, client: TestClient, session: Session, student_token: str,
        student_user, active_ad
    ):
        """Student cannot apply twice to the same ad (unique constraint)."""
        from app.models.application import Application
        existing_app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(existing_app)
        session.flush()

        payload = {
            "ad_id": active_ad.id,
            "cv_path": "/uploads/cvs/student_cv.pdf",
            "motivational_letter_path": "/uploads/letters/motivation.pdf",
            "phone": "+38761234567",
        }
        response = client.post(
            "/applications/",
            json=payload,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_non_student_cannot_create_application(
        self, client: TestClient, admin_token: str, active_ad
    ):
        """Only students (members) can create applications."""
        payload = {
            "ad_id": active_ad.id,
            "cv_path": "/uploads/cvs/student_cv.pdf",
            "motivational_letter_path": "/uploads/letters/motivation.pdf",
            "phone": "+38761234567",
        }
        # Admin trying to create application
        response = client.post(
            "/applications/",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code in [403, 400]


# ============================================================
# GET /applications/{application_id} — Get single application
# ============================================================

class TestGetApplication:

    def test_admin_can_get_any_application(
        self, client: TestClient, session: Session, admin_token: str,
        student_user, active_ad, company_user
    ):
        """Admin can view any application."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.get(
            f"/applications/{app.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == app.id

    def test_student_can_get_their_own_application(
        self, client: TestClient, session: Session, student_token: str,
        student_user, active_ad
    ):
        """Student can view their own application."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.get(
            f"/applications/{app.id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200

    def test_student_cannot_get_other_student_application(
        self, client: TestClient, session: Session, student_token: str,
          company_user
    ):
        """Student cannot view another student's application."""
        isolated_ad = Ad(
            company_id=company_user.id,
            title="Isolated Ad For Test",
            type=AdType.internship,
            field="IT",
            location="Sarajevo",
            description="Testing isolation.",
            deadline=date.today() + timedelta(days=10),
            duration_months=3,
            status=AdStatus.active,
        )
        session.add(isolated_ad)
        session.flush()

        
        other_student = User(
            email="other@test.ba",
            full_name="Other Student",
            password_hash=hash_password("password"),
            role=UserRole.member,
            is_active=True,
        )
        session.add(other_student)
        session.flush()
        session.refresh(other_student)

        app = Application(
            user_id=other_student.id,
            ad_id=isolated_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.get(
            f"/applications/{app.id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 403

    def test_get_non_existent_application(self, client: TestClient, admin_token: str):
        """Getting non-existent application returns 404."""
        response = client.get(
            "/applications/99999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 404


# ============================================================
# PATCH /applications/{application_id} — Admin update status
# ============================================================

class TestUpdateApplicationAdmin:

    def test_admin_can_update_application_status(
        self, client: TestClient, session: Session, admin_token: str,
        student_user, active_ad, company_user
    ):
        """Admin can update application status."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        payload = {
            "status": "accepted",
            "admin_feedback": "Good CV!",
        }
        response = client.patch(
            f"/applications/{app.id}",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["admin_feedback"] == "Good CV!"

    def test_non_admin_cannot_update_status(
        self, client: TestClient, session: Session, student_token: str,
        student_user, active_ad, company_user
    ):
        """Non-admins cannot update application status."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()

        payload = {"status": "rejected"}
        response = client.patch(
            f"/applications/{app.id}",
            json=payload,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 403


# ============================================================
# PATCH /applications/company/{application_id} — Company update
# ============================================================

class TestUpdateApplicationCompany:

    def test_company_can_update_their_application(
        self, client: TestClient, session: Session, company_token: str,
        company_user, student_user, active_ad
    ):
        """Company can update application status for their ads."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        payload = {
            "status": "accepted",
            "admin_feedback": "Welcome!",
        }
        response = client.patch(
            f"/applications/company/{app.id}",
            json=payload,
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"

    def test_company_cannot_update_other_company_application(
        self, client: TestClient, session: Session, company_token: str,
        student_user, other_company_ad
    ):
        """Company cannot update applications for ads they don't own."""
        app = Application(
            user_id=student_user.id,
            ad_id=other_company_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        payload = {"status": "rejected"}
        response = client.patch(
            f"/applications/company/{app.id}",
            json=payload,
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 403
        assert "You do not have access to alter this application." in response.json()["detail"]

    def test_company_accept_notifies_student(
        self, client: TestClient, session: Session, company_token: str,
        company_user, student_user, active_ad
    ):
        """When company accepts, student gets notification."""
        
        
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        payload = {"status": "accepted"}
        response = client.patch(
            f"/applications/company/{app.id}",
            json=payload,
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 200
        
        # Check that notification was created
        notifications = session.exec(
            select(Notification).where(Notification.user_id == student_user.id)
        ).all()
        assert len(notifications) > 0

    def test_company_accept_multiple_fills_spots_expires_ad(
        self, client: TestClient, session: Session, company_token: str,
        company_user, active_ad
    ):
        """When company accepts enough applications to fill spots, ad expires."""
        from app.models.application import Application
        from app.models.user import User, UserRole
        from app.core.security import hash_password
        
        # Create 2 students
        student1 = User(
            email="student1@test.ba",
            full_name="Student 1",
            password_hash=hash_password("pwd"),
            role=UserRole.member,
        )
        student2 = User(
            email="student2@test.ba",
            full_name="Student 2",
            password_hash=hash_password("pwd"),
            role=UserRole.member,
        )
        session.add(student1)
        session.add(student2)
        session.flush()
        session.refresh(student1)
        session.refresh(student2)
        
        # Create 2 applications
        app1 = Application(
            user_id=student1.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test1.pdf",
            motivational_letter_path="/uploads/letters/test1.pdf",
            phone="+38761234567",
        )
        app2 = Application(
            user_id=student2.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test2.pdf",
            motivational_letter_path="/uploads/letters/test2.pdf",
            phone="+38761234568",
        )
        session.add(app1)
        session.add(app2)
        session.flush()
        session.refresh(app1)
        session.refresh(app2)

        # Accept first
        response1 = client.patch(
            f"/applications/company/{app1.id}",
            json={"status": "accepted"},
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response1.status_code == 200

        # Accept second (should fill 2 spots of active_ad which has spots=2)
        response2 = client.patch(
            f"/applications/company/{app2.id}",
            json={"status": "accepted"},
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response2.status_code == 200

        # Check that ad is now expired
        session.refresh(active_ad)
        assert active_ad.status == AdStatus.expired


# ============================================================
# DELETE /applications/{application_id} — Soft delete
# ============================================================

class TestDeleteApplication:

    def test_admin_can_delete_application(
        self, client: TestClient, session: Session, admin_token: str,
        student_user, active_ad, company_user
    ):
        """Admin can archive (soft delete) an application."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.delete(
            f"/applications/{app.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 204

        # Verify it's archived (soft delete)
        session.refresh(app)
        assert app.is_archived == True

    def test_non_admin_cannot_delete_application(
        self, client: TestClient, session: Session, student_token: str,
        student_user, active_ad, company_user
    ):
        """Non-admins cannot delete applications."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()

        response = client.delete(
            f"/applications/{app.id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 403

    def test_delete_non_existent_application(self, client: TestClient, admin_token: str):
        """Deleting non-existent application returns 404."""
        response = client.delete(
            "/applications/99999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 404


# ============================================================
# GET /applications/company/application/{application_id} — Company view
# ============================================================

class TestGetCompanyApplication:

    def test_company_can_view_their_application(
        self, client: TestClient, session: Session, company_token: str,
        company_user, student_user, active_ad
    ):
        """Company can view application for their ad."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=active_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.get(
            f"/applications/company/application/{app.id}",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == app.id

    def test_company_cannot_view_other_company_application(
        self, client: TestClient, session: Session, company_token: str,
        student_user, other_company_ad
    ):
        """Company cannot view applications for ads they don't own."""
        from app.models.application import Application
        app = Application(
            user_id=student_user.id,
            ad_id=other_company_ad.id,
            cv_path="/uploads/cvs/test.pdf",
            motivational_letter_path="/uploads/letters/test.pdf",
            phone="+38761234567",
        )
        session.add(app)
        session.flush()
        session.refresh(app)

        response = client.get(
            f"/applications/company/application/{app.id}",
            headers={"Authorization": f"Bearer {company_token}"}
        )
        assert response.status_code == 403


# ============================================================
# POST /applications/upload-cv — File upload
# ============================================================

class TestUploadCv:

    def test_student_can_upload_cv(
        self, client: TestClient, student_token: str
    ):
        """Student can upload a PDF CV."""
        import io
        
        pdf_content = b"%PDF-1.4\n%mock pdf content"
        file = io.BytesIO(pdf_content)
        
        response = client.post(
            "/applications/upload-cv",
            files={"file": ("cv.pdf", file, "application/pdf")},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "path" in data
        assert "applications" in data["path"]
        assert data["path"].endswith(".pdf")

    def test_cannot_upload_non_pdf(
        self, client: TestClient, student_token: str
    ):
        """Cannot upload non-PDF files."""
        import io
        
        file = io.BytesIO(b"Not a PDF")
        
        response = client.post(
            "/applications/upload-cv",
            files={"file": ("cv.txt", file, "text/plain")},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 400
        assert "must have a .pdf extension" in response.json()["detail"]

    def test_cannot_upload_oversized_file(
        self, client: TestClient, student_token: str
    ):
        """Cannot upload file larger than 5MB."""
        import io
        
        # Create a file larger than 5MB
        large_content = b"x" * (6 * 1024 * 1024)
        file = io.BytesIO(large_content)
        
        response = client.post(
            "/applications/upload-cv",
            files={"file": ("cv.pdf", file, "application/pdf")},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 400
        assert "5 MB" in response.json()["detail"]

    def test_unauthenticated_cannot_upload(
        self, client: TestClient
    ):
        """Unauthenticated users cannot upload."""
        import io
        
        file = io.BytesIO(b"%PDF mock")
        
        response = client.post(
            "/applications/upload-cv",
            files={"file": ("cv.pdf", file, "application/pdf")},
        )
        assert response.status_code == 401
