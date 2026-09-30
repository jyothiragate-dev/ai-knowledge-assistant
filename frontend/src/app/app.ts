import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import {
  ChangeDetectorRef,
  Component
} from '@angular/core';
import { FormsModule } from '@angular/forms';

interface Source {
  source: string;
  page: string | null;
}

interface QueryResponse {
  answer: string;
  sources: Source[];
}

interface UploadResponse {
  message: string;
  filename: string;
  pages: number;
  chunks: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  query = '';
  answer = '';
  sources: Source[] = [];

  isLoading = false;
  errorMessage = '';

  selectedFile: File | null = null;
  uploadMessage = '';
  isUploading = false;

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  askQuestion(): void {

    const question = this.query.trim();

    if (!question || this.isLoading) {
      return;
    }

    this.isLoading = true;
    this.answer = '';
    this.sources = [];
    this.errorMessage = '';

    this.http
      .post<QueryResponse>(
        'http://localhost:8080/api/query',
        {
          query: question
        }
      )
      .subscribe({

        next: (response) => {

          this.answer = response.answer;

          this.sources =
            response.sources ?? [];

          this.isLoading = false;

          this.cdr.detectChanges();
        },

        error: (error) => {

          console.error(
            'Query failed:',
            error
          );

          this.errorMessage =
            'Unable to get an answer right now. Please try again.';

          this.isLoading = false;

          this.cdr.detectChanges();
        }
      });
  }


  onFileSelected(event: Event): void {

    const input =
      event.target as HTMLInputElement;

    this.selectedFile =
      input.files?.[0] ?? null;

    this.uploadMessage = '';
  }


  uploadDocument(): void {

    if (
      !this.selectedFile ||
      this.isUploading
    ) {
      return;
    }

    const formData = new FormData();

    formData.append(
      'file',
      this.selectedFile
    );

    this.isUploading = true;
    this.uploadMessage = '';

    this.http
      .post<UploadResponse>(
        'http://localhost:8000/documents/upload',
        formData
      )
      .subscribe({

        next: (response) => {

          this.uploadMessage =
            response.message;

          this.isUploading = false;

          this.selectedFile = null;

          this.cdr.detectChanges();
        },

        error: (error) => {

          console.error(
            'Upload failed:',
            error
          );

          this.uploadMessage =
            'Unable to upload the document. Please try again.';

          this.isUploading = false;

          this.cdr.detectChanges();
        }
      });
  }


  clearConversation(): void {

    this.query = '';
    this.answer = '';
    this.sources = [];
    this.errorMessage = '';
  }
}