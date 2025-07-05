"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, Controller, ControllerRenderProps, FieldValues } from "react-hook-form";
import * as z from "zod";
import { CheckIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import Link from "next/link";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Logo from "@/components/landing/logo";

// Updated form schema with new fields and purpose values
const formSchema = z.object({
  purpose: z.enum(["wishlistFree", "wishlistPaid", "question"]),
  fullName: z.string().min(1, "Full name is required"),
  email: z.string().email({ message: "Please enter a valid email address." }),
  company: z.string().optional(),
  jobTitle: z.string().optional(),
  teamSize: z.string().optional(),
  source: z.string().optional(),
  challenges: z.string().optional(),
  urgency: z.string().optional(),
  cardNumber: z.string().optional(),
  expiry: z.string().optional(),
  cvc: z.string().optional(),
  questionText: z.string().optional(),
}).superRefine((data, ctx) => {
  if (data.purpose === "wishlistPaid") {
    if (!data.cardNumber) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["cardNumber"],
        message: "Card number is required",
      });
    }
    if (!data.expiry) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["expiry"],
        message: "Expiry date is required",
      });
    }
    if (!data.cvc) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["cvc"],
        message: "CVC is required",
      });
    }
  } else if (data.purpose === "question") {
    if (!data.questionText) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["questionText"],
        message: "Question is required",
      });
    }
  }
});

type FormValues = z.infer<typeof formSchema>;

export default function EarlyAccessPage() {
  const { toast } = useToast();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      purpose: "wishlistFree",
    },
  });

  const watchPurpose = form.watch("purpose");

  function onSubmit(data: FormValues) {
    console.log("Form submission:", data);
    toast({
      title: "Success!",
      description: data.purpose === "wishlistPaid"
        ? "You've joined our priority wishlist! Payment processed successfully."
        : data.purpose === "wishlistFree"
        ? "You've been added to our wishlist!"
        : "Your question has been submitted! We'll contact you soon.",
    });
    form.reset();
  }

  // Define InputField props interface to fix type error
  interface InputFieldProps {
    name: keyof FormValues;
    label: string;
    placeholder?: string;
  }

  const InputField = ({ name, label, placeholder }: InputFieldProps) => (
    <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Input placeholder={placeholder} {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );

  return (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-2">
      
      {/* Left: Form */}
      <div className="flex flex-col justify-center px-8 py-12 bg-[#fffaf5] h-full overflow-y-auto">
        <div className="max-w-lg mx-auto w-full space-y-8">
          
          <Logo />
          <h2 className="text-3xl font-bold mb-6">Get in Touch</h2>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              
              {/* Purpose Selection */}
              <FormField
                control={form.control}
                name="purpose"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-lg text-gray-800 mb-2">What would you like to do?</FormLabel>
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        value={field.value}
                        className="flex flex-col space-y-2"
                      >
                        <FormItem className="flex items-center space-x-2">
                          <FormControl>
                            <RadioGroupItem value="wishlistFree" />
                          </FormControl>
                          <FormLabel className="cursor-pointer">Join Wishlist (Free)</FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-2">
                          <FormControl>
                            <RadioGroupItem value="wishlistPaid" />
                          </FormControl>
                          <FormLabel className="cursor-pointer">Join Wishlist (Priority - $10 Refundable)</FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-2">
                          <FormControl>
                            <RadioGroupItem value="question" />
                          </FormControl>
                          <FormLabel className="cursor-pointer">Ask a Question</FormLabel>
                        </FormItem>
                      </RadioGroup>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Common Fields */}
              <div className="space-y-4">
                <InputField name="fullName" label="Full Name" placeholder="Your name" />
                <InputField name="email" label="Email" placeholder="you@example.com" />
                <InputField name="company" label="Company (optional)" placeholder="Your company" />
                <InputField name="jobTitle" label="Job Title (optional)" placeholder="Your role" />
                
                <FormField
                  control={form.control}
                  name="teamSize"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Team Size (optional)</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select team size" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="1-10">1-10</SelectItem>
                          <SelectItem value="11-50">11-50</SelectItem>
                          <SelectItem value="51-200">51-200</SelectItem>
                          <SelectItem value="201-500">201-500</SelectItem>
                          <SelectItem value="500+">500+</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              {/* Conditional Fields for Wishlist */}
              {watchPurpose === "wishlistFree" || watchPurpose === "wishlistPaid" ? (
                <div className="space-y-4">
                  <InputField name="source" label="How did you hear about us?" placeholder="Google, LinkedIn, etc." />
                  <InputField name="challenges" label="What challenges are you trying to solve?" placeholder="Your answer" />
                  
                  <FormField
                    control={form.control}
                    name="urgency"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>How important is this for you?</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select urgency" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="notUrgent">Not urgent</SelectItem>
                            <SelectItem value="soon">Soon</SelectItem>
                            <SelectItem value="veryUrgent">Very urgent</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  {watchPurpose === "wishlistPaid" && (
                    <Card className="bg-gray-100 border">
                      <CardHeader>
                        <CardTitle className="flex justify-between items-center">
                          <span>Payment Amount</span>
                          <span className="font-bold text-blue-600">$10.00 USD</span>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <InputField name="cardNumber" label="Card Number" placeholder="1234 5678 9012 3456" />
                        <div className="grid grid-cols-2 gap-4">
                          <InputField name="expiry" label="Expiry Date" placeholder="MM/YY" />
                          <InputField name="cvc" label="CVC" placeholder="123" />
                        </div>
                        <p className="text-sm text-gray-500">Fully refundable anytime before launch.</p>
                      </CardContent>
                    </Card>
                  )}
                </div>
              ) : null}

              {/* Conditional for Ask a Question */}
              {watchPurpose === "question" && (
                <FormField
                  control={form.control}
                  name="questionText"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Your Question</FormLabel>
                      <FormControl>
                        <Textarea placeholder="Type your question here..." rows={4} {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}

              {/* Submit Button */}
              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg">
                {watchPurpose === "wishlistPaid" ? "Join Wishlist (Priority)" :
                watchPurpose === "wishlistFree" ? "Join Wishlist" :
                "Submit Question"}
              </Button>

              <p className="text-center text-xs text-gray-500">
                By submitting, you agree to our{" "}
                <Link href="/privacy" className="text-blue-500 underline">Privacy Policy</Link>.
              </p>

            </form>
          </Form>
        </div>
      </div>

      {/* Right: Image */}
      <div
        className="hidden lg:flex flex-col justify-center items-center relative bg-cover bg-center"
        style={{ backgroundImage: "url('/painterly-bg.png')" }}
      >
        <div className="flex flex-col">
            <div className="bg-blue-500 text-white rounded-xl p-6 shadow-none w-full px-auto">
              <h2 className="text-2xl font-bold mb-4">🚀 Early Access Offer</h2>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <CheckIcon className="w-5 h-5 text-green-300 mr-2" />
                  <span>Exclusive discounts for early adopters</span>
                </li>
                <li className="flex items-center">
                  <CheckIcon className="w-5 h-5 text-green-300 mr-2" />
                  <span>Priority access to new features</span>
                </li>
                <li className="flex items-center">
                  <CheckIcon className="w-5 h-5 text-green-300 mr-2" />
                  <span>Direct line to our development team</span>
                </li>
              </ul>
            </div>

            {/* Bottom: Heading and Subheading */}
            <div className="mt-8">
              <h1 className="text-4xl font-bold mb-4">Join the Future Today</h1>
              <p className="text-xl text-gray-400">
                Be among the first to experience our cutting-edge platform and transform the way you work.
              </p>
            </div>
          </div>
      </div>
    </div>
  );
}