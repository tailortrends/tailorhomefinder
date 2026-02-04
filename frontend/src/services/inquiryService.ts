/**
 * Service for handling property inquiries and contact form submissions
 */

const API_BASE_URL = 'http://localhost:8000';

export interface ContactFormData {
  name: string;
  email: string;
  phone: string;
  message: string;
  property_id: string;
  property_address?: string;
  property_price?: number;
  inquiry_type?: 'general' | 'schedule_tour' | 'request_info' | 'make_offer';
}

export interface InquiryResponse {
  success: boolean;
  message: string;
  inquiry_id?: string;
}

export interface Inquiry {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  message: string;
  inquiry_type: string;
  property_id: string | null;
  property_address: string | null;
  property_price: number | null;
  status: 'new' | 'read' | 'responded' | 'closed';
  email_sent: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface InquiryListResponse {
  total: number;
  inquiries: Inquiry[];
  limit: number;
  offset: number;
}

export interface InquiryStats {
  total_inquiries: number;
  new_inquiries: number;
  responded_inquiries: number;
  tour_requests: number;
  offer_inquiries: number;
}

class InquiryService {
  private baseUrl = API_BASE_URL;

  /**
   * Submit a contact form inquiry
   */
  async submitContactForm(data: ContactFormData): Promise<InquiryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/inquiries/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: data.name,
          email: data.email,
          phone: data.phone,
          message: data.message,
          property_id: data.property_id,
          property_address: data.property_address,
          property_price: data.property_price,
          inquiry_type: data.inquiry_type || 'general'
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to submit inquiry: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error submitting contact form:', error);
      throw error;
    }
  }

  /**
   * Get list of inquiries (admin only)
   */
  async getInquiries(params: {
    status?: string;
    property_id?: string;
    limit?: number;
    offset?: number;
  } = {}): Promise<InquiryListResponse> {
    try {
      const queryParams = new URLSearchParams();

      if (params.status) queryParams.append('status', params.status);
      if (params.property_id) queryParams.append('property_id', params.property_id);
      if (params.limit) queryParams.append('limit', params.limit.toString());
      if (params.offset) queryParams.append('offset', params.offset.toString());

      const url = `${this.baseUrl}/api/inquiries/?${queryParams.toString()}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`Failed to fetch inquiries: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching inquiries:', error);
      throw error;
    }
  }

  /**
   * Get a single inquiry by ID
   */
  async getInquiry(id: string): Promise<Inquiry> {
    try {
      const response = await fetch(`${this.baseUrl}/api/inquiries/${id}`);

      if (!response.ok) {
        throw new Error(`Inquiry not found: ${id}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Error fetching inquiry ${id}:`, error);
      throw error;
    }
  }

  /**
   * Update inquiry status (admin only)
   */
  async updateInquiryStatus(id: string, status: 'new' | 'read' | 'responded' | 'closed'): Promise<Inquiry> {
    try {
      const response = await fetch(`${this.baseUrl}/api/inquiries/${id}/status`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });

      if (!response.ok) {
        throw new Error(`Failed to update inquiry status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Error updating inquiry ${id}:`, error);
      throw error;
    }
  }

  /**
   * Get inquiry statistics (admin only)
   */
  async getInquiryStats(): Promise<InquiryStats> {
    try {
      const response = await fetch(`${this.baseUrl}/api/inquiries/stats/overview`);

      if (!response.ok) {
        throw new Error('Failed to fetch inquiry stats');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching inquiry stats:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const inquiryService = new InquiryService();
